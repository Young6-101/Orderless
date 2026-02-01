import { HeroUIProvider } from "@heroui/react";
import { Route, Routes } from "react-router-dom";
import { Layout } from "./layouts/layout";

// 只留下这个我们刚刚创建的文件
import IndexPage from "./pages/index"; 

function App() {
  return (
    <HeroUIProvider>
      <Layout>
        <Routes>
          {/* 只保留一个根路由，删掉 docs 和 pricing */}
          <Route path="/" element={<IndexPage />} />
        </Routes>
      </Layout>
    </HeroUIProvider>
  );
}

export default App;