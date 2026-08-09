from services.quiz_service import fetch_quiz
from utils.file_utils import cleanup
from config import OUTPUT_VIDEO, OUTPUT_DIR
from services.facebook_service import upload_video_to_facebook
from services.video_service import generate_images, create_video
import os


def run_pipeline():
    print("📁 Creating output dir...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("📥 Fetching quiz...")
    quiz, is_fallback = fetch_quiz()
    

    # ❌ Stop if fallback
    if is_fallback:
        print("🚫 Fallback detected → stopping pipeline")
        return

    # ❌ Safety check
    if not quiz or len(quiz) == 0:
        print("❌ No quiz data received")
        return

    print(f"✅ {len(quiz)} questions loaded")

    # =========================
    # 🖼️ Generate images
    # =========================
    print("🖼️ Generating images...")
    images = generate_images(quiz)

    if not images:
        print("❌ No images generated")
        return

    # =========================
    # 🎬 Create video
    # =========================
    print("🎬 Creating video...")
    create_video(images, OUTPUT_VIDEO)

    if not os.path.exists(OUTPUT_VIDEO):
        print("❌ Video not created. Skipping Facebook upload.")
        return

    # =========================
    # 📤 Upload to Facebook
    # =========================
    print("📤 Uploading to Facebook...")

    upload_video_to_facebook(
        OUTPUT_VIDEO,
        caption="""📊English Exam Focus Caption

📚 Daily practice for serious aspirants

🎯 SSC | UPSC | Banking | Railway | RAS | IAS 

💬 Drop your answer below

#sscpreparation #upsc #bankexam #railwayexam
#mocktest #aptitude #reasoning #govtjobs #studyreels"""
    )

    # =========================
    # 🧹 Cleanup
    # =========================
    print("🧹 Cleaning up...")
    cleanup(images)

    print("✅ Done!")