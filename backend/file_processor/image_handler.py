from langchain_ollama import ChatOllama
import base64
from pathlib import Path

class ImageDescriber:
    def __init__(self, model_name: str = "moondream"):
        """
        Initialize the image description model using Ollama's moondream.
        moondream is a lightweight vision model perfect for generating image descriptions.
        """
        print(f"--- [LOG] Initializing vision model: {model_name} ---")
        self.model = ChatOllama(model=model_name, temperature=0.3)
    
    def describe_image(self, image_path: str, prompt: str = "Describe this image in detail.") -> str:
        """
        Generate a textual description of an image using moondream.
        
        Args:
            image_path: Path to the image file
            prompt: Custom prompt for image description (default: general description)
            
        Returns:
            str: Textual description of the image
        """
        try:
            # Read and encode the image
            image_path_obj = Path(image_path)
            if not image_path_obj.exists():
                return f"[Image not found: {image_path}]"
            
            with open(image_path, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Create message with image
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_data]
                }
            ]
            
            # Get description from moondream
            response = self.model.invoke(messages)
            description = response.content if isinstance(response.content, str) else str(response.content)
            
            print(f"--- [LOG] Generated description for {image_path_obj.name} ---")
            return description
            
        except Exception as e:
            print(f"--- [ERROR] Failed to describe image {image_path}: {e} ---")
            return f"[Error describing image: {image_path}]"
    
    def batch_describe(self, image_paths: list[str], prompt: str = "Describe this image in detail.") -> list[str]:
        """
        Generate descriptions for multiple images.
        
        Args:
            image_paths: List of image file paths
            prompt: Custom prompt for image description
            
        Returns:
            list[str]: List of image descriptions
        """
        descriptions = []
        for image_path in image_paths:
            desc = self.describe_image(image_path, prompt)
            descriptions.append(desc)
        return descriptions
    
    def analyze_pattern(self, image_paths: list[str]) -> str:
        """
        Analyze multiple images to identify common patterns.
        
        This method describes each image individually, then asks the model
        to synthesize common patterns across all samples.
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            str: Synthesized analysis of common patterns
        """
        if not image_paths:
            return "No design samples provided."
        
        print(f"--- [LOG] Analyzing {len(image_paths)} images for patterns ---")
        
        # First, describe each design
        individual_descriptions = []
        for idx, image_path in enumerate(image_paths):
            desc = self.describe_image(
                image_path,
                prompt="Describe this image in detail. Focus on the key visual elements, style, composition, and any notable patterns or characteristics."
            )
            individual_descriptions.append(f"Sample {idx+1}: {desc}")
        
        # Then, synthesize patterns (using text-only LLM call)
        synthesis_prompt = f"""Based on these image descriptions, identify common patterns and themes:

{chr(10).join(individual_descriptions)}

Summarize:
1. Common visual themes and recurring elements
2. Shared style or aesthetic characteristics
3. Notable patterns across the samples
4. Key takeaways and insights"""

        try:
            response = self.model.invoke(synthesis_prompt)
            synthesis = response.content if isinstance(response.content, str) else str(response.content)
            return synthesis
        except Exception as e:
            print(f"--- [ERROR] Pattern synthesis failed: {e} ---")
            return "\n\n".join(individual_descriptions)
