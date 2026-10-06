"""Example usage for Video Clip Semantic Segmentation."""
from client import VideoClipSemanticSegmenter

if __name__ == "__main__":
    segments = [
        {"start": 0.0, "end": 20.0, "text": "Here is the key breakthrough we discovered during deployment."},
        {"start": 20.0, "end": 60.0, "text": "Our agent throughput immediately jumped by three hundred percent."}
    ]
    res = VideoClipSemanticSegmenter.segment_transcript(segments)
    print("Clips extracted:", res["clips_generated"])
    for c in res["top_clips"]:
        print(f"[{c['start_sec']}s - {c['end_sec']}s] Score {c['viral_potential_score']}: {c['summary_text']}")
