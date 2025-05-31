// App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import BlogGenerator from "./components/BlogGenerator";
import CalendarView from "./components/CalendarView";
import Dashboard from "./components/Dashboard";
import Sidebar from "./components/Sidebar";

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-gray-900 text-white">
        <Sidebar />
        <div className="flex-1 p-4 overflow-y-auto">
          <Routes>
            <Route path="/" element={<BlogGenerator />} />
            <Route path="/calendar" element={<CalendarView />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
