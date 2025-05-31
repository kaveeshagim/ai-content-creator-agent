import { useEffect, useState } from "react";
import { getCalendarData } from "../api/blogApi";
import { saveAs } from "file-saver";

interface CalendarEntry {
  date: string;
  title: string;
  slug: string;
}

const CalendarView = () => {
  const [entries, setEntries] = useState<CalendarEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedMonth, setSelectedMonth] = useState<string>("all");
  const [selectedYear, setSelectedYear] = useState<string>("all");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getCalendarData();
        const sortedData = data.sort(
          (a: CalendarEntry, b: CalendarEntry) =>
            new Date(b.date).getTime() - new Date(a.date).getTime()
        );
        setEntries(sortedData);
      } catch (err) {
        console.error("Failed to fetch calendar data", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDownload = () => {
    const csv = ["Date,Title,Link"].concat(
      entries.map(
        (entry) =>
          `${entry.date},"${entry.title}",https://kaveeshagim.github.io/ai-content-creator-agent/${entry.slug}.html`
      )
    );
    const blob = new Blob([csv.join("\n")], {
      type: "text/csv;charset=utf-8;",
    });
    saveAs(blob, "blog_calendar.csv");
  };

  const filteredEntries = entries.filter((entry) => {
    const matchesSearch = entry.title
      .toLowerCase()
      .includes(search.toLowerCase());
    const matchesMonth =
      selectedMonth === "all" ||
      new Date(entry.date).getMonth() + 1 === parseInt(selectedMonth);
    const matchesYear =
      selectedYear === "all" ||
      new Date(entry.date).getFullYear().toString() === selectedYear;
    return matchesSearch && matchesMonth && matchesYear;
  });

  const uniqueYears = Array.from(
    new Set(entries.map((e) => new Date(e.date).getFullYear().toString()))
  );

  return (
    <div className="max-w-6xl mx-auto p-4 text-black dark:text-white bg-gray-800">
      <h2 className="text-2xl font-bold mb-4">📅 Blog Calendar</h2>

      <div className="flex flex-wrap gap-4 mb-4 items-center">
        <input
          type="text"
          placeholder="🔍 Search title..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="p-2 border rounded w-full sm:w-1/2"
        />
        <select
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(e.target.value)}
          className="border p-2 rounded bg-white text-black dark:bg-gray-800 dark:text-white"
        >
          <option value="all">All Months</option>
          {Array.from({ length: 12 }, (_, i) => (
            <option key={i + 1} value={i + 1}>
              {new Date(0, i).toLocaleString("default", { month: "long" })}
            </option>
          ))}
        </select>
        <select
          value={selectedYear}
          onChange={(e) => setSelectedYear(e.target.value)}
          className="border p-2 rounded bg-white text-black dark:bg-gray-800 dark:text-white"
        >
          <option value="all">All Years</option>
          {uniqueYears.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded cursor-pointer"
          onClick={handleDownload}
        >
          📥 Download CSV
        </button>
      </div>

      {loading ? (
        <p>Loading calendar data...</p>
      ) : filteredEntries.length === 0 ? (
        <p>No blogs match the current filter.</p>
      ) : (
        <div className="bg-gray-100 dark:bg-gray-800 shadow rounded p-4">
          <table className="w-full table-auto border-collapse mb-6">
            <thead>
              <tr>
                <th className="text-left p-2 border-b">Date</th>
                <th className="text-left p-2 border-b">Title</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntries.map((entry, index) => (
                <tr key={index} className="border-t">
                  <td className="p-2">{entry.date}</td>
                  <td className="p-2">{entry.title}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h3 className="text-xl font-semibold mb-2">🔗 Blog Links</h3>
          <ul className="list-disc pl-6">
            {filteredEntries.map((entry, index) => (
              <li key={index} className="mb-1">
                📌 {entry.date}:{" "}
                <a
                  href={`https://kaveeshagim.github.io/ai-content-creator-agent/${entry.slug}.html`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 no-underline"
                >
                  {entry.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default CalendarView;
