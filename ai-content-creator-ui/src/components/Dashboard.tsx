import { useEffect, useState } from "react";
import { getAnalyticsData } from "../api/blogApi";
import { BarChart2 } from "lucide-react";
import { saveAs } from "file-saver";
import { Bar } from "react-chartjs-2";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { LineElement, PointElement, TimeScale, Title } from "chart.js";
import "chartjs-adapter-date-fns";
ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  TimeScale,
  Title
);

interface Post {
  slug: string;
  date: string;
  reading_time: string;
  summary_bullets: string;
  seo_tags: string[];
}

interface AnalyticsResponse {
  total_blogs: number;
  posts: Post[];
  unique_tags: string[];
  tag_counts: Record<string, number>;
}

const Dashboard = () => {
  const [data, setData] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [chartView, setChartView] = useState<"Weekly" | "Monthly">("Weekly");

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await getAnalyticsData();
        setData(response);
      } catch (error) {
        console.error("Error fetching analytics", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  const handleDownload = () => {
    if (!data) return;
    const csv = ["Slug,Date,Reading Time,Tags,Summary"].concat(
      data.posts.map(
        (post) =>
          `${post.slug},${post.date},${post.reading_time},"${post.seo_tags.join(
            ", "
          )}","${post.summary_bullets}"
        `
      )
    );
    const blob = new Blob([csv.join("\n")], {
      type: "text/csv;charset=utf-8;",
    });
    saveAs(blob, "analytics.csv");
  };

  const filteredPosts = data?.posts.filter((post) => {
    const matchesSearch =
      post.slug.toLowerCase().includes(search.toLowerCase()) ||
      post.summary_bullets?.toLowerCase().includes(search.toLowerCase());
    const matchesTags =
      selectedTags.length === 0 ||
      selectedTags.some((tag) => post.seo_tags.includes(tag));
    return matchesSearch && matchesTags;
  });

  const barChartData = data
    ? {
        labels: Object.keys(data.tag_counts),
        datasets: [
          {
            label: "Top SEO Tags",
            data: Object.values(data.tag_counts),
            backgroundColor: "#4B8BBE",
          },
        ],
      }
    : { labels: [], datasets: [] };

  const lineChartData = {
    labels: data?.posts.map((post) => post.date),
    datasets: [
      {
        label: "Blogs per Day",
        data: data?.posts.map((_, index) => index + 1), // fake cumulative count
        borderColor: "#4B8BBE",
        backgroundColor: "rgba(75, 139, 190, 0.4)",
        tension: 0.3,
      },
    ],
  };

  const lineChartOptions = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Blog Generation Over Time",
      },
    },
    scales: {
      x: {
        type: "time" as const,
        time: {
          unit: "day" as const,
        },
        title: {
          display: true,
          text: "Date",
        },
      },
      y: {
        title: {
          display: true,
          text: "Cumulative Blog Count",
        },
      },
    },
  };

  return (
    <div className="max-w-7xl mx-auto p-4 text-black dark:text-white">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <BarChart2 className="w-6 h-6" /> AI Content Creator Analytics
      </h2>

      {loading ? (
        <p>Loading dashboard...</p>
      ) : data ? (
        <>
          <div className="bg-green-700 text-white p-2 rounded mb-4">
            ✅ Loaded {data.total_blogs} blog posts
          </div>

          <button
            className="bg-gray-600 text-white px-4 py-2 rounded mb-4 cursor-pointer"
            onClick={handleDownload}
          >
            📥 Download All Metadata as CSV
          </button>

          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">
              📊 Blog Generation Trends
            </h2>
            <div className="flex gap-4 mb-4">
              <label>
                <input
                  type="radio"
                  value="Weekly"
                  checked={chartView === "Weekly"}
                  onChange={() => setChartView("Weekly")}
                />{" "}
                Weekly
              </label>
              <label>
                <input
                  type="radio"
                  value="Monthly"
                  checked={chartView === "Monthly"}
                  onChange={() => setChartView("Monthly")}
                />{" "}
                Monthly
              </label>
            </div>
            <Line data={lineChartData} options={lineChartOptions} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-gray-100 dark:bg-gray-800 p-4 shadow rounded">
              <h2 className="font-semibold text-lg">📝 Total Blogs</h2>
              <p className="text-2xl">{data.total_blogs}</p>
            </div>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 shadow rounded">
              <h2 className="font-semibold text-lg">⏱ Avg Reading Time</h2>
              <p className="text-2xl">2 min</p>
            </div>
            <div className="bg-gray-100 dark:bg-gray-800 p-4 shadow rounded">
              <h2 className="font-semibold text-lg">🏷️ Unique Tags</h2>
              <p className="text-2xl">{data.unique_tags.length}</p>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-2">
              📆 Blog Posting Heatmap
            </h2>
            <CalendarHeatmap
              startDate={new Date("2025-01-01")}
              endDate={new Date()}
              values={data.posts.map((post) => ({
                date: post.date,
                count: 1, // or use a counter if multiple posts per day
              }))}
            />
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-2">
              🏷️ Most Common SEO Tags
            </h2>
            <Bar data={barChartData} options={{ indexAxis: "y" }} />
          </div>

          <div className="bg-gray-100 dark:bg-gray-800 shadow rounded p-4 mb-6">
            <h2 className="text-xl font-semibold mb-4">
              📚 Blog Archive & Filters
            </h2>

            <input
              type="text"
              className="w-full border rounded p-2 text-white mb-4"
              placeholder="Search by keyword in title or summary"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            <select
              multiple
              className="w-full border rounded p-2 mb-4 text-white"
              value={selectedTags}
              onChange={(e) =>
                setSelectedTags(
                  Array.from(e.target.selectedOptions, (o) => o.value)
                )
              }
            >
              {data.unique_tags.map((tag, i) => (
                <option key={i} value={tag}>
                  {tag}
                </option>
              ))}
            </select>

            <p className="text-lg font-semibold mb-2">
              🗂️ Showing {filteredPosts?.length} blog(s)
            </p>
            <div className="space-y-2">
              {filteredPosts?.map((post, idx) => (
                <details
                  key={idx}
                  className="bg-gray-200 dark:bg-gray-700 p-4 rounded"
                >
                  <summary className="font-semibold cursor-pointer">
                    {post.slug.replace(/-/g, " ")}
                  </summary>
                  <div className="mt-2">
                    <p>
                      📅 <strong>Date:</strong> {post.date}
                    </p>
                    <p>
                      ⏱ <strong>Reading Time:</strong> {post.reading_time}
                    </p>
                    <p>
                      🏷️ <strong>Tags:</strong>{" "}
                      {(post.seo_tags || []).join(", ")}
                    </p>

                    <p>
                      🧠 <strong>Summary:</strong>
                    </p>
                    <ul className="list-disc ml-6">
                      {(post.summary_bullets?.split("\n") || []).map(
                        (line, i) => (
                          <li key={i}>{line}</li>
                        )
                      )}
                    </ul>

                    <a
                      href={`https://kaveeshagim.github.io/ai-content-creator-agent/${post.slug}.html`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 underline mt-2 inline-block"
                    >
                      🔗 View Blog
                    </a>
                  </div>
                </details>
              ))}
            </div>
          </div>
        </>
      ) : (
        <p>No analytics data found.</p>
      )}
    </div>
  );
};

export default Dashboard;
