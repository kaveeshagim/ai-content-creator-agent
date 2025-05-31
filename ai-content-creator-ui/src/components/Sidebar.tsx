import { Link, useLocation } from "react-router-dom";
import { PencilIcon, CalendarDaysIcon, BarChart2Icon } from "lucide-react"; // optional icon pack (e.g., lucide-react)

export default function Sidebar() {
  const { pathname } = useLocation();

  const navItems = [
    {
      label: "Blog Generator",
      icon: <PencilIcon size={18} />,
      to: "/",
    },
    {
      label: "Calendar View",
      icon: <CalendarDaysIcon size={18} />,
      to: "/calendar",
    },
    {
      label: "Dashboard",
      icon: <BarChart2Icon size={18} />,
      to: "/dashboard",
    },
  ];

  return (
    <aside className="w-64 bg-gray-900 text-white p-6 min-h-screen shadow-lg">
      <h2 className="text-2xl font-bold mb-8 tracking-wide flex items-center gap-2">
        🧠 AI Creator
      </h2>

      <ul className="space-y-2">
        {navItems.map(({ label, icon, to }) => {
          const isActive = pathname === to;
          return (
            <li key={label}>
              <Link
                to={to}
                className={`flex items-center gap-3 px-4 py-2 rounded-md transition-colors ${
                  isActive
                    ? "bg-blue-600 text-white"
                    : "hover:bg-gray-800 text-gray-300"
                }`}
              >
                {icon}
                <span className="text-sm font-medium">{label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </aside>
  );
}
