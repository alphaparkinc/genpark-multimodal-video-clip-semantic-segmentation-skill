"""MCP server for Video Clip Semantic Segmentation."""
import sys
import json
from client import VideoClipSemanticSegmenter

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "segment_video_transcript",
                "description": "Segments timed video transcripts into candidate viral clips",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "timed_segments": {"type": "array"},
                        "max_clip_duration_sec": {"type": "integer"}
                    },
                    "required": ["timed_segments"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "segment_video_transcript":
            args = params.get("arguments", {})
            res = VideoClipSemanticSegmenter.segment_transcript(
                args.get("timed_segments", []),
                args.get("max_clip_duration_sec", 60)
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
