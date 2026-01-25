import argparse
import sys
import os
from dubsmart.core.pipeline import DubbingPipeline
from dubsmart.utils import get_logger

def main():
    parser = argparse.ArgumentParser(description="Dubsmart AI: Multilingual Audio Dubbing")
    parser.add_argument("--input", required=True, help="Input audio/video file")
    parser.add_argument("--src", default="en", help="Source language code")
    parser.add_argument("--tgt", required=True, help="Target language code")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    logger = get_logger(__name__)
    
    output_path = args.output or f"output/dubbed_{args.tgt}.wav"
    
    try:
        pipeline = DubbingPipeline(src_lang=args.src, tgt_lang=args.tgt)
        result = pipeline.process(args.input, output_path)
        logger.info(f"Dubbing successful! Result: {result}")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
