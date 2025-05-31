import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import BlogGenerator from "./components/BlogGenerator";
import CalendarView from "./components/CalenderView";
import Dashboard from "./components/Dashboard";
import Sidebar from "./components/Sidebar";

function App() {
  return (
    <Router>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 p-4">
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
