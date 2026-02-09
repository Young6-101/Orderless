import { useState } from "react";

export interface Stack {
  id: string;
  name: string;
  createdAt: number;
}

export const useStacks = () => {
  const [stacks, setStacks] = useState<Stack[]>([]);
  const addStack = (name: string) => {
    const newStack: Stack = {
      id: Math.random().toString(36).substr(2, 9),
      name,
      createdAt: Date.now()
    };
    setStacks((prev) => [...prev, newStack]);
  };
  return { stacks, addStack };
};