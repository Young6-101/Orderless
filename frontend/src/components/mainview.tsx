import React from "react";
import { Sidebar } from "./sidebar";

interface MainViewProps {
  children?: React.ReactNode;
}

export default function MainView({ children }: MainViewProps) {
  return (
    // flex-row ensures Sidebar and Main stay side-by-side
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden">
      {/* Fixed Sidebar */}
      <Sidebar />

      {/* Dynamic Content Area */}
      <main className="flex-1 overflow-y-auto relative">
        {/* If no children provided, show a default welcome message */}
        {children || (
          <div className="p-8 flex flex-col gap-4">
            <h1 className="text-4xl font-bold italic">Main Workspace</h1>
            <p className="text-default-500">
              Select an item from the sidebar to get started.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}