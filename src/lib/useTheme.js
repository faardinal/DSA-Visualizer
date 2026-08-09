import { useState, useEffect } from "react";

// Always default to dark. The user can toggle to light with the button.
const getInitialTheme = () => {
  const stored = localStorage.getItem("dsa-theme");
  return stored === "light" ? "light" : "dark";
};

// Apply dark class synchronously before first React render so the page
// never flashes white background.
if (typeof document !== "undefined") {
  const initial = getInitialTheme();
  if (initial === "dark") {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
}

export function useTheme() {
  const [theme, setTheme] = useState(getInitialTheme);

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    localStorage.setItem("dsa-theme", theme);
  }, [theme]);

  const toggle = () => setTheme((t) => (t === "dark" ? "light" : "dark"));

  return { theme, toggle };
}
