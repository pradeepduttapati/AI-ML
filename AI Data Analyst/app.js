import { useState } from "react";
import "@/App.css";
import axios from "axios";
import { Upload, FileText, BarChart3, Send, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Toaster, toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [dataset, setDataset] = useState(null);
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setDataset(response.data);
      toast.success("Dataset uploaded successfully!");
      setMessages([
        {
          role: "assistant",
          content: `Dataset "${response.data.filename}" loaded successfully! It contains ${response.data.shape.rows} rows and ${response.data.shape.columns} columns. Ask me anything about your data!`,
        },
      ]);
    } catch (error) {
      console.error("Upload error:", error);
      toast.error(error.response?.data?.detail || "Failed to upload dataset");
    } finally {
      setUploading(false);
    }
  };

  const handleQuery = async () => {
    if (!question.trim() || loading) return;

    const userMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await axios.post(`${API}/query`, { question });
      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
        insights: response.data.insights,
        chart: response.data.chart,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Query error:", error);
      toast.error(error.response?.data?.detail || "Failed to process query");
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I encountered an error processing your question.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    "What are the top trends in this dataset?",
    "Show me the summary statistics",
    "Which column has the highest values?",
    "Create a visualization of the data",
    "What are the key insights?",
  ];

  return (
    <div className="h-screen flex flex-col bg-white">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur-md">
        <div className="px-6 py-4">
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900" style={{ fontFamily: 'Manrope, sans-serif' }} data-testid="app-title">
            <Sparkles className="inline-block w-8 h-8 mr-2 text-indigo-600" />
            AI Data Analyst
          </h1>
          <p className="text-slate-600 mt-1" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Natural Language Data Exploration</p>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 grid grid-cols-1 md:grid-cols-12 gap-0 overflow-hidden">
        {/* Left Sidebar */}
        <aside className="col-span-1 md:col-span-3 lg:col-span-2 border-r border-slate-200 bg-slate-50/50 p-4 overflow-y-auto" data-testid="sidebar">
          {/* Upload Section */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-3" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Upload Dataset</h3>
            <label htmlFor="file-upload" className="block">
              <div className="border-2 border-dashed border-slate-300 rounded-lg p-4 hover:border-indigo-500 transition-colors cursor-pointer bg-white" data-testid="upload-area">
                <Upload className="w-8 h-8 mx-auto text-slate-400 mb-2" />
                <p className="text-sm text-center text-slate-600">Click to upload CSV or Excel</p>
                {uploading && <p className="text-xs text-center text-indigo-600 mt-2">Uploading...</p>}
              </div>
              <input
                id="file-upload"
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileUpload}
                className="hidden"
                disabled={uploading}
                data-testid="file-input"
              />
            </label>
          </div>

          {/* Dataset Info */}
          {dataset && (
            <div data-testid="dataset-info">
              <h3 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-3" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Dataset Info</h3>
              <Card className="mb-4 shadow-sm">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm flex items-center gap-2" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>
                    <FileText className="w-4 h-4" />
                    {dataset.filename}
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-sm text-slate-600">
                  <p data-testid="dataset-rows">Rows: {dataset.shape.rows}</p>
                  <p data-testid="dataset-columns">Columns: {dataset.shape.columns}</p>
                </CardContent>
              </Card>

              <h3 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-3" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Columns</h3>
              <div className="space-y-1" data-testid="columns-list">
                {dataset.columns.map((col, idx) => (
                  <div key={idx} className="text-sm px-3 py-2 bg-white rounded border border-slate-200 text-slate-700">
                    {col}
                  </div>
                ))}
              </div>
            </div>
          )}
        </aside>

        {/* Main Chat Area */}
        <main className="col-span-1 md:col-span-9 lg:col-span-7 flex flex-col relative" data-testid="main-chat">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center max-w-lg">
                  <BarChart3 className="w-16 h-16 mx-auto text-slate-300 mb-4" />
                  <h2 className="text-2xl font-semibold text-slate-900 mb-2" style={{ fontFamily: 'Manrope, sans-serif' }}>Upload a dataset to begin</h2>
                  <p className="text-slate-600" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Start by uploading a CSV or Excel file, then ask questions about your data in natural language.</p>
                </div>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  data-testid={`message-${msg.role}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-3 ${
                      msg.role === "user"
                        ? "bg-indigo-600 text-white"
                        : "bg-slate-100 text-slate-900 border border-slate-200"
                    }`}
                    style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}
                  >
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    {msg.insights && msg.insights.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-slate-300" data-testid="insights-list">
                        <p className="font-semibold text-sm mb-2">Key Insights:</p>
                        <ul className="list-disc list-inside space-y-1 text-sm">
                          {msg.insights.map((insight, i) => (
                            <li key={i}>{insight}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {msg.chart && (
                      <div className="mt-3" data-testid="chart-image">
                        <img src={msg.chart} alt="Chart" className="rounded border border-slate-200" />
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex justify-start" data-testid="loading-indicator">
                <div className="bg-slate-100 border border-slate-200 rounded-lg px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Suggested Questions */}
          {dataset && messages.length === 1 && (
            <div className="px-6 pb-4" data-testid="suggested-questions">
              <p className="text-sm font-semibold text-slate-700 mb-2" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Try asking:</p>
              <div className="flex flex-wrap gap-2">
                {suggestedQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => setQuestion(q)}
                    className="text-xs px-3 py-1.5 bg-white border border-slate-300 rounded-full hover:border-indigo-500 hover:text-indigo-600 transition-colors"
                    data-testid={`suggested-question-${idx}`}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="border-t border-slate-200 bg-white/80 backdrop-blur-md p-4">
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder={dataset ? "Ask a question about your data..." : "Upload a dataset first"}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleQuery()}
                disabled={!dataset || loading}
                className="flex-1 border-slate-200 focus:ring-2 focus:ring-indigo-500/20"
                data-testid="query-input"
              />
              <Button
                onClick={handleQuery}
                disabled={!dataset || !question.trim() || loading}
                className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm"
                data-testid="send-button"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </main>

        {/* Right Panel - Preview */}
        {dataset && (
          <aside className="hidden lg:block col-span-3 border-l border-slate-200 p-4 overflow-y-auto bg-white" data-testid="preview-panel">
            <h3 className="text-sm font-semibold uppercase tracking-widest text-slate-500 mb-3" style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}>Data Preview</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-xs border border-slate-200 rounded">
                <thead className="bg-slate-100">
                  <tr>
                    {dataset.columns.map((col, idx) => (
                      <th key={idx} className="px-2 py-1 text-left font-semibold text-slate-700 border-b border-slate-200">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {dataset.preview.map((row, idx) => (
                    <tr key={idx} className="border-b border-slate-100">
                      {dataset.columns.map((col, colIdx) => (
                        <td key={colIdx} className="px-2 py-1 text-slate-600">
                          {String(row[col] || "")}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </aside>
        )}
      </div>
    </div>
  );
}

export default App;
