import { Listbox, ListboxItem, Divider } from "@heroui/react";
// Using icons that actually exist in your icons.tsx
import { Logo, GithubIcon, DiscordIcon, HeartFilledIcon } from "./icons"; 
import { ThemeSwitch } from "./theme-switch"; 

export const Sidebar = () => {
  return (
    <div className="h-screen w-64 border-r border-divider p-4 flex flex-col bg-content1/50">
      {/* Header with your actual Logo and ThemeSwitch */}
      <div className="flex items-center justify-between mb-6 px-2 py-2">
        <div className="flex items-center gap-2">
          <Logo size={32} />
          <span className="font-bold text-xl tracking-tight">Orderless</span>
        </div>
        <ThemeSwitch />
      </div>

      <Divider className="mb-6" />

      {/* Navigation Menu using existing icons */}
      <nav className="flex-1">
        <Listbox 
          aria-label="Main Navigation"
          variant="flat"
          className="p-0 gap-1"
        >
          <ListboxItem
            key="home"
            startContent={<Logo size={20} />} // Reusing Logo as a placeholder
          >
            Home
          </ListboxItem>
          
          <ListboxItem
            key="github"
            startContent={<GithubIcon size={20} />}
          >
            Source Code
          </ListboxItem>

          <ListboxItem
            key="community"
            startContent={<DiscordIcon size={20} />}
          >
            Community
          </ListboxItem>
        </Listbox>
      </nav>

      {/* Footer with Heart Icon */}
      <div className="mt-auto p-2 flex items-center gap-2 text-xs text-default-400">
        Made with <HeartFilledIcon size={14} className="text-danger" /> by Orderless
      </div>
    </div>
  );
};