import { motion } from "framer-motion";
import "./StackIcon.css";

interface StackIconProps {
    name: string;
    description?: string;
    onClick?: () => void;
}

export const StackIcon = ({ name, description, onClick }: StackIconProps) => {
    return (
        <motion.div
            whileHover={{ y: -16 }}
            transition={{ duration: 0.48, ease: [0.23, 1, 0.32, 1] }}
            onClick={onClick}
            className="stack-card"
        >
            <div className="stack-content">
                {/* Icon */}
                <svg
                    className="stack-icon"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path d="M20 9V5H4V9H20ZM20 11H4V19H20V11ZM3 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3ZM5 12H8V17H5V12ZM5 6H7V8H5V6ZM9 6H11V8H9V6Z" />
                </svg>

                {/* Text */}
                <div className="stack-text">
                    <h3>{name}</h3>
                    {description && <p>{description}</p>}
                </div>
            </div>
        </motion.div>
    );
};
