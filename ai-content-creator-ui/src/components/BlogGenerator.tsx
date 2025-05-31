import { useState } from "react";
import { generateBlog, saveBlog, suggestTopics } from "../api/blogApi";

interface BlogResult {
  topic: string;
  blog: string;
  social_posts: string;
  citations: string;
  tweet_thread: string;
  linkedin_post: string;
}

const BlogGenerator = () => {
  const [topic, setTopic] = useState("");
  const [queue, setQueue] = useState<string[]>([]);
  const [tone, setTone] = useState("professional");
  const [audience, setAudience] = useState("general audience");
  const [outline, setOutline] = useState("");
  const [showOutlineBox, setShowOutlineBox] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<BlogResult | null>(null);
  const [trendingCategory, setTrendingCategory] = useState("tech");
  const [suggestedTopics, setSuggestedTopics] = useState<string[]>([]);

  const addToQueue = () => {
    if (topic.trim()) {
      setQueue([...queue, topic.trim()]);
      setTopic("");
    }
  };

  const generate = async (queuedTopic: string) => {
    setLoading(true);
    try {
      const res = await generateBlog({
        topic: queuedTopic,
        tone,
        audience,
        outline: outline || undefined,
      });
      setResult(res);
      await saveBlog({
        topic: res.topic,
        blog: res.blog,
        captions: res.social_posts,
        citations: res.citations,
      });
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const generateNext = async () => {
    if (queue.length > 0) {
      const next = queue[0];
      setQueue(queue.slice(1));
      await generate(next);
    }
  };

  const runFullQueue = async () => {
    while (queue.length > 0) {
      await generateNext();
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4 bg-gray-800">
      <h2 className="text-2xl font-bold mb-4">🧠 AI Blog Generator</h2>

      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter blog topic"
        className="border p-2 w-full mb-2 rounded"
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={addToQueue}
      >
        ➕ Add to Queue
      </button>

      {queue.length > 0 && (
        <div className="mt-4">
          <h2 className="text-lg font-semibold">⏳ Topics in Queue</h2>
          <ul className="list-disc pl-6">
            {queue.map((q, idx) => (
              <li key={idx}>{q}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-4">
        <label className="block mb-1">🎨 Tone</label>
        <select
          className="border p-2 w-full rounded bg-white text-black dark:bg-gray-800 dark:text-white"
          value={tone}
          onChange={(e) => setTone(e.target.value)}
        >
          <option>professional</option>
          <option>casual</option>
          <option>witty</option>
          <option>inspirational</option>
          <option>conversational</option>
        </select>
      </div>

      <div className="mt-4">
        <label className="block mb-1">🎯 Audience</label>
        <select
          className="border p-2 w-full rounded bg-white text-black dark:bg-gray-800 dark:text-white"
          value={audience}
          onChange={(e) => setAudience(e.target.value)}
        >
          <option>general audience</option>
          <option>beginners</option>
          <option>developers</option>
          <option>business professionals</option>
          <option>CTOs</option>
          <option>students</option>
        </select>
      </div>

      <div className="mt-4">
        <label className="block mb-1">
          <input
            type="checkbox"
            checked={showOutlineBox}
            onChange={() => setShowOutlineBox(!showOutlineBox)}
          />
          <span className="ml-2">🧠 Show outline input box</span>
        </label>
        {showOutlineBox && (
          <textarea
            value={outline}
            onChange={(e) => setOutline(e.target.value)}
            placeholder="Write or edit your outline..."
            className="border p-2 w-full rounded mt-2"
            rows={6}
          ></textarea>
        )}
      </div>

      {queue.length > 0 && (
        <div className="flex gap-4 mt-6">
          <button
            className="bg-green-600 text-white px-4 py-2 rounded"
            onClick={generateNext}
            disabled={loading}
          >
            🚀 {loading ? "Generating..." : "Generate Next"}
          </button>
          <button
            className="bg-purple-600 text-white px-4 py-2 rounded"
            onClick={runFullQueue}
            disabled={loading}
          >
            🚂 Run Full Queue
          </button>
        </div>
      )}

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-2">📈 Need Ideas?</h2>
        <div className="flex items-center gap-4 mb-2">
          <label htmlFor="category">Select Category:</label>
          <select
            id="category"
            className="border p-2 rounded bg-white text-black dark:bg-gray-800 dark:text-white"
            value={trendingCategory}
            onChange={(e) => setTrendingCategory(e.target.value)}
          >
            <option value="tech">Tech</option>
            <option value="ai">AI</option>
            <option value="devops">DevOps</option>
            <option value="startups">Startups</option>
            <option value="webdev">Web Development</option>
          </select>
          <button
            className="bg-indigo-600 text-white px-3 py-1 rounded cursor-pointer"
            onClick={async () => {
              const res = await suggestTopics(trendingCategory);
              setSuggestedTopics(res.topics || []);
            }}
          >
            Generate Topics
          </button>
        </div>

        <ul className="list-disc pl-6">
          {suggestedTopics.map((t, i) => (
            <li key={i}>
              <button
                className="text-blue-600 underline"
                onClick={() => setTopic(t)}
              >
                {t}
              </button>
            </li>
          ))}
        </ul>
      </div>

      {result && (
        <div className="mt-8 bg-gray-800 p-4 rounded">
          <h2 className="text-xl font-bold mb-2">📝 Blog Output</h2>

          <div className="mb-4">
            <h3 className="font-semibold mb-1">📌 Blog</h3>
            <pre className="whitespace-pre-wrap mb-2 bg-gray-800 p-2 rounded border overflow-auto max-h-96">
              {result.blog}
            </pre>
            <a
              href={`data:text/markdown;charset=utf-8,${encodeURIComponent(
                result.blog
              )}`}
              download={`${result.topic}.md`}
              className="text-blue-600 underline"
            >
              📥 Download Blog (.md)
            </a>
          </div>

          <div className="mb-4">
            <h3 className="font-semibold mb-1">📣 Captions</h3>
            <pre className="whitespace-pre-wrap mb-2 bg-gray-800 p-2 rounded border overflow-auto max-h-96">
              {result.social_posts}
            </pre>
            <a
              href={`data:text/plain;charset=utf-8,${encodeURIComponent(
                result.social_posts
              )}`}
              download={`${result.topic}_captions.txt`}
              className="text-blue-600 underline"
            >
              📥 Download Captions (.txt)
            </a>
          </div>

          <div className="mb-4">
            <h3 className="font-semibold mb-1">🔗 Citations</h3>
            <pre className="whitespace-pre-wrap mb-2 bg-gray-800 p-2 rounded border overflow-auto max-h-96">
              {result.citations}
            </pre>
            <a
              href={`data:text/plain;charset=utf-8,${encodeURIComponent(
                result.citations
              )}`}
              download={`${result.topic}_citations.txt`}
              className="text-blue-600 underline"
            >
              📥 Download Citations (.txt)
            </a>
          </div>

          <div className="mb-4">
            <h3 className="font-semibold mb-1">🐦 Tweet Thread</h3>
            <pre className="whitespace-pre-wrap mb-2 bg-gray-800 p-2 rounded border overflow-auto max-h-96">
              {result.tweet_thread}
            </pre>
            <a
              href={`data:text/plain;charset=utf-8,${encodeURIComponent(
                result.tweet_thread
              )}`}
              download={`${result.topic}_thread.txt`}
              className="text-blue-600 underline"
            >
              📥 Download Tweet Thread (.txt)
            </a>
          </div>

          <div className="mb-4">
            <h3 className="font-semibold mb-1">📰 LinkedIn Post</h3>
            <pre className="whitespace-pre-wrap mb-2 bg-gray-800 p-2 rounded border overflow-auto max-h-96">
              {result.linkedin_post}
            </pre>
            <a
              href={`data:text/plain;charset=utf-8,${encodeURIComponent(
                result.linkedin_post
              )}`}
              download={`${result.topic}_linkedin.txt`}
              className="text-blue-600 underline"
            >
              📥 Download LinkedIn Post (.txt)
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default BlogGenerator;
