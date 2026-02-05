
import { useEffect, useMemo, useRef, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

type PredictResult = {
  prediction: string;
  confidence: number;
  samples: number;
};

type Mode = "upload" | "stream";

function App() {
  const BACKEND_URL = "http://127.0.0.1:8000";
  const WS_URL = "ws://127.0.0.1:8000/ws/ecg";

  const [mode, setMode] = useState<Mode>("upload");

  // upload mode
  const [file, setFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<PredictResult | null>(null);

  // streaming mode
  const [connected, setConnected] = useState(false);
  const [streamResult, setStreamResult] = useState<PredictResult | null>(null);
  const [streaming, setStreaming] = useState(false);

  // live ECG buffer for chart
  const [ecgData, setEcgData] = useState<{ x: number; y: number }[]>([]);
  const tRef = useRef(0);

  const wsRef = useRef<WebSocket | null>(null);
  const timerRef = useRef<number | null>(null);

  const [loading, setLoading] = useState(false);

  const handlePredictUpload = async () => {
    if (!file) {
      alert("Please upload a CSV file first!");
      return;
    }

    try {
      setLoading(true);
      setUploadResult(null);

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${BACKEND_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        alert(`Backend error (${res.status}): ${text}`);
        return;
      }

      const data = (await res.json()) as PredictResult;
      setUploadResult(data);
    } catch (err) {
      alert("Error connecting to backend! Check console.");
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  const connectWs = () => {
    if (wsRef.current && (wsRef.current.readyState === 0 || wsRef.current.readyState === 1)) {
      return;
    }

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => {
      setConnected(false);
      setStreaming(false);
    };
    ws.onerror = () => {
      setConnected(false);
      setStreaming(false);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        // backend sends: { prediction, confidence, samples }
        setStreamResult({
          prediction: msg.prediction,
          confidence: msg.confidence,
          samples: msg.samples ?? 0,
        });
      } catch (e) {
        // ignore
      }
    };
  };

  const disconnectWs = () => {
    if (timerRef.current) {
      window.clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setStreaming(false);

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setConnected(false);
  };

  // generate a realistic-ish ECG-like waveform (demo streaming)
  // later you can replace this with real device stream
  const nextEcgPoint = useMemo(() => {
    // simple ECG-ish pattern: baseline + spikes
    let phase = 0;
    return () => {
      phase += 1;

      const base = Math.sin(phase / 12) * 0.05 + Math.sin(phase / 55) * 0.03;

      // occasional QRS spike
      const spikePos = phase % 60;
      let spike = 0;
      if (spikePos === 10) spike = 0.9;
      if (spikePos === 11) spike = -0.25;
      if (spikePos === 12) spike = 0.15;

      const noise = (Math.random() - 0.5) * 0.02;

      return base + spike + noise;
    };
  }, []);

  const startStreaming = () => {
    if (!wsRef.current || wsRef.current.readyState !== 1) {
      alert("WebSocket not connected. Click Connect first.");
      return;
    }

    if (timerRef.current) return;

    setStreaming(true);
    setEcgData([]);
    tRef.current = 0;

    // send a sliding window to backend for live inference
    const WINDOW = 5000; // backend pads/truncates anyway
    let windowBuf: number[] = [];

    timerRef.current = window.setInterval(() => {
      const y = nextEcgPoint();
      const x = tRef.current++;
      setEcgData((prev) => {
        const next = [...prev, { x, y }];
        // keep only latest 300 points visible on chart
        return next.length > 300 ? next.slice(next.length - 300) : next;
      });

      windowBuf.push(y);
      if (windowBuf.length > WINDOW) windowBuf = windowBuf.slice(windowBuf.length - WINDOW);

      // send inference request every ~0.5s (adjust as you want)
      if (x % 25 === 0) {
        const payload = windowBuf.join(",");
        wsRef.current?.send(payload);
      }
    }, 20); // 20ms ~ 50Hz visual update
  };

  const stopStreaming = () => {
    if (timerRef.current) {
      window.clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setStreaming(false);
  };

  useEffect(() => {
    return () => {
      disconnectWs();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center p-6">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-3xl">
        <h1 className="text-3xl font-bold text-center text-blue-600">
          ECG Arrhythmia Detection
        </h1>

        <div className="flex gap-2 justify-center mt-5">
          <button
            className={`px-4 py-2 rounded-xl border ${
              mode === "upload" ? "bg-blue-600 text-white" : "bg-white"
            }`}
            onClick={() => setMode("upload")}
          >
            Upload CSV
          </button>
          <button
            className={`px-4 py-2 rounded-xl border ${
              mode === "stream" ? "bg-blue-600 text-white" : "bg-white"
            }`}
            onClick={() => setMode("stream")}
          >
            Live Streaming
          </button>
        </div>

        {mode === "upload" && (
          <>
            <p className="text-gray-600 text-center mt-4">
              Upload ECG CSV file for prediction
            </p>

            <input
              type="file"
              accept=".csv"
              className="w-full mt-6 p-3 border rounded-xl bg-white"
              onChange={(e) => {
                if (e.target.files && e.target.files.length > 0) {
                  setFile(e.target.files[0]);
                }
              }}
            />

            <button
              onClick={handlePredictUpload}
              className="w-full mt-4 bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700 transition"
            >
              {loading ? "Predicting..." : "Predict Rhythm"}
            </button>

            {uploadResult && (
              <div className="mt-6 p-4 bg-green-100 border border-green-300 rounded-xl">
                <h2 className="text-xl font-semibold text-green-700">
                  Prediction Result
                </h2>
                <p className="mt-2 text-gray-800">
                  Rhythm: {uploadResult.prediction}
                </p>
                <p className="text-gray-800">
                  Confidence: {uploadResult.confidence}
                </p>
                <p className="text-gray-800">
                  Samples Used: {uploadResult.samples}
                </p>
              </div>
            )}
          </>
        )}

        {mode === "stream" && (
          <>
            <p className="text-gray-600 text-center mt-4">
              Live ECG chart + live prediction using WebSocket
            </p>

            <div className="flex gap-3 justify-center mt-4">
              <button
                onClick={connectWs}
                className="px-4 py-2 rounded-xl bg-gray-900 text-white hover:bg-gray-800"
              >
                Connect
              </button>

              <button
                onClick={disconnectWs}
                className="px-4 py-2 rounded-xl bg-gray-200 hover:bg-gray-300"
              >
                Disconnect
              </button>

              {!streaming ? (
                <button
                  onClick={startStreaming}
                  className="px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700"
                  disabled={!connected}
                >
                  Start Stream
                </button>
              ) : (
                <button
                  onClick={stopStreaming}
                  className="px-4 py-2 rounded-xl bg-red-600 text-white hover:bg-red-700"
                >
                  Stop Stream
                </button>
              )}
            </div>

            <div className="mt-4 text-center text-sm text-gray-700">
              Connection: {connected ? "Connected" : "Not connected"}
            </div>

            <div className="mt-6 p-4 border rounded-2xl bg-white">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={ecgData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="x" />
                    <YAxis domain={[-1.2, 1.2]} />
                    <Tooltip />
                    <Line type="monotone" dataKey="y" dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {streamResult && (
              <div className="mt-6 p-4 bg-green-100 border border-green-300 rounded-xl">
                <h2 className="text-xl font-semibold text-green-700">
                  Live Prediction
                </h2>
                <p className="mt-2 text-gray-800">
                  Rhythm: {streamResult.prediction}
                </p>
                <p className="text-gray-800">
                  Confidence: {streamResult.confidence}
                </p>
                <p className="text-gray-800">
                  Samples Used: {streamResult.samples}
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
