import { HeroUIProvider } from "@heroui/react";
import MainView from "./components/mainview";

function App() {
  return (
    // HeroUIProvider is required for styles and theme context to work
    <HeroUIProvider>
      <MainView>
        {/* Everything inside MainView will appear in the right-hand area */}
        <div className="p-8">
          <section className="max-w-4xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Current Project: Frontend</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-6 rounded-xl border border-divider bg-content2">
                <p className="text-sm font-medium">Status</p>
                <p className="text-lg text-success font-bold">Connected to Localhost</p>
              </div>
              <div className="p-6 rounded-xl border border-divider bg-content2">
                <p className="text-sm font-medium">Architecture</p>
                <p className="text-lg font-bold uppercase">Flattened Component Tree</p>
              </div>
            </div>
          </section>
        </div>
      </MainView>
    </HeroUIProvider>
  );
}

export default App;