import React from "react";
import { Sidebar } from "../pages/sidebar"; // 确保这里的路径指向你写的那个侧边栏

export const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex h-screen w-full">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  );
};