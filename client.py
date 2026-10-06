"""Multimodal Video Clip Semantic Segmentation.
100% Python Standard Library.
"""

class VideoClipSemanticSegmenter:
    """Extracts timestamp boundaries, semantic scenes, and viral clip candidate segments."""
    
    @staticmethod
    def segment_transcript(timed_segments: list, max_clip_duration_sec: int = 60) -> dict:
        candidates = []
        current_cluster = []
        current_duration = 0.0
        
        interest_markers = ["crucial", "secret", "never", "breakthrough", "mistake", "key is", "how we made"]
        
        for seg in timed_segments:
            start = seg.get("start", 0.0)
            end = seg.get("end", 0.0)
            dur = max(0.0, end - start)
            
            if current_duration + dur > max_clip_duration_sec and current_cluster:
                clip_text = " ".join(s.get("text", "") for s in current_cluster)
                score = 85 if any(h in clip_text.lower() for h in interest_markers) else 65
                candidates.append({
                    "start_sec": current_cluster[0]["start"],
                    "end_sec": current_cluster[-1]["end"],
                    "duration_sec": round(current_cluster[-1]["end"] - current_cluster[0]["start"], 2),
                    "viral_potential_score": score,
                    "summary_text": clip_text[:120] + "..." if len(clip_text) > 120 else clip_text
                })
                current_cluster = []
                current_duration = 0.0
                
            current_cluster.append(seg)
            current_duration += dur
            
        if current_cluster:
            clip_text = " ".join(s.get("text", "") for s in current_cluster)
            candidates.append({
                "start_sec": current_cluster[0]["start"],
                "end_sec": current_cluster[-1]["end"],
                "duration_sec": round(current_cluster[-1]["end"] - current_cluster[0]["start"], 2),
                "viral_potential_score": 75,
                "summary_text": clip_text[:120] + "..." if len(clip_text) > 120 else clip_text
            })
            
        return {
            "total_segments_analyzed": len(timed_segments),
            "clips_generated": len(candidates),
            "top_clips": sorted(candidates, key=lambda x: x["viral_potential_score"], reverse=True)
        }
