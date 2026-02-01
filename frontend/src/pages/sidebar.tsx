import { Listbox, ListboxItem, Card, Avatar, Divider } from "@heroui/react";

export const Sidebar = () => {
  return (
    // h-screen 让侧边栏占满整个屏幕高度，w-64 设置宽度
    <div className="h-screen w-64 border-r border-divider p-4 flex flex-col gap-4">
      
      {/* 顶部：用户信息/Logo */}
      <div className="flex items-center gap-3 px-2 py-4">
        <Avatar src="https://i.pravatar.cc/150" size="sm" />
        <span className="font-bold text-lg">My Project</span>
      </div>

      <Divider />

      {/* 中间：导航菜单 */}
      <Listbox aria-label="Main Navigation" variant="flat">
        <ListboxItem key="dashboard" startContent={<span>🏠</span>}>
          仪表盘
        </ListboxItem>
        <ListboxItem key="projects" startContent={<span>📂</span>}>
          我的项目
        </ListboxItem>
        <ListboxItem key="team" startContent={<span>👥</span>}>
          团队管理
        </ListboxItem>
        <ListboxItem key="settings" startContent={<span>⚙️</span>}>
          系统设置
        </ListboxItem>
      </Listbox>

      {/* 底部：辅助信息（自动推到底部） */}
      <div className="mt-auto">
        <Card className="bg-primary/10 p-3 shadow-none">
          <p className="text-xs text-primary">当前版本: v1.0.0</p>
        </Card>
      </div>
    </div>
  );
};