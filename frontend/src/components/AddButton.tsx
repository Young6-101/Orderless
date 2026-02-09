import { Button } from "@heroui/react";

interface AddButtonProps {
    onPress: () => void;
}

export const AddButton = ({ onPress }: AddButtonProps) => {
    return (
        <Button
            onPress={onPress}
            className="w-20 h-20 bg-[#0a86ce] text-white text-4xl rounded-full shadow-2xl hover:scale-110 transition-transform font-light"
        >
            +
        </Button>
    );
};
