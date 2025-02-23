from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from models import db, User, AttendanceStudents, TeachersAttendance
from forms import RegisterForm, LoginForm , AttendanceForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_bcrypt import Bcrypt
import numpy as np
import cv2
import os
from datetime import datetime


app = Flask(__name__)

# Configuration
app.config['SECURITY_PASSWORD_SALT'] = "MY_SECRET"
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECRET_KEY'] = 'c9fae1f0910dc43606221b0ebb4e46ce749f5abcc11d128a8cae155ee7eb5676'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize Extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

# Create tables before first request
with app.app_context():
    db.create_all()

# User Loader
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id) or None
@app.route("/")
def home():
    return render_template("base.html")
# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, role=form.role.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html', form=form)

# Protected Dashboard Route
@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():

        form=AttendanceForm()
        return render_template("dashboard.html", user=current_user,form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Attendance creation (Teachers Only)
@app.route('/attendance_')
@login_required
def attendance_():
    if current_user.role != "2":  # Only teachers can create attendance
        return "Access Forbidden: Only teachers can create attendance.", 403

    FPS = 30
    DURATION = 2
    TOTAL_FRAMES = FPS * DURATION
    pattern = np.random.choice([0, 1], size=TOTAL_FRAMES+9)
    new_value = [1,1,1,1,1,1,1,0,0]  # Value to add at the front

    pattern = np.concatenate((np.array(new_value), pattern))

    pattern_str = ''.join(map(str, pattern.tolist()))



    new_attendance = TeachersAttendance(
    pattern=pattern_str,
    username=current_user.username,
    email=current_user.email,
    date=datetime.utcnow()  # Optional, since default is already set
    )

# Add to session and commit
    db.session.add(new_attendance)
    db.session.commit()

    return render_template('attendance.html', pattern=pattern.tolist(), FPS=FPS,attID=new_attendance.attID)

@app.route('/video_capture', methods=['GET', 'POST'])
@login_required
def video_capture():
    form = AttendanceForm()
    if form.validate_on_submit():
        session["attendance_code"] = form.username.data
        session["roll_number"] = form.roll_number.data
    if not session["attendance_code"] or not session["roll_number"]:
        return jsonify({"error": "Missing attendance code or roll number"}), 400

    return render_template("video_capture.html")



UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



@app.route('/upload', methods=['POST'])
@login_required
def upload_video():
    # Check if 'video' is in request
    if 'video' not in request.files:
        return jsonify({"error": "No video file received"}), 400

    video = request.files['video']

    # nsure file is not empty
    if video.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Define save path & save video
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_video.webm')
    video.save(filename)

    print(f"video uploaded successfully at: {filename}")  # Debugging print

    return jsonify({
        "message": "Video uploaded successfully",
        "redirect_url": url_for('verify_recording', _external=True)  # ✅ Redirects to verification page
    })



# Pattern Extraction from Video
def extract_binary_sequence(video_path):
    """Extracts binary sequence from recorded video based on brightness."""
    cap = cv2.VideoCapture(video_path)

    FPS = 30
    DURATION = 2
    TOTAL_FRAMES = FPS * DURATION

    frame_count = 0
    binary_sequence = []
    recording = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray_frame)

        if not recording and avg_brightness >= 128:
            recording = True
            print(f"First white frame detected at frame {frame_count} (Brightness: {avg_brightness})")

        if recording:
            bit = 1 if avg_brightness < 128 else 0
            binary_sequence.append(bit)

            if len(binary_sequence) >= TOTAL_FRAMES:
                break

        frame_count += 1

    cap.release()
    return ''.join(map(str, binary_sequence))

# Find 3 Largest Common Substrings
def find_longest_common_substrings(s1, s2):
    """Finds the three longest non-overlapping common substrings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    substrings = []

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                substr = s1[i - dp[i][j]: i]
                substrings.append((dp[i][j], substr))

    substrings.sort(reverse=True, key=lambda x: x[0])
    selected_substrings = []
    used_ranges_s1 = set()
    used_ranges_s2 = set()

    for length, substr in substrings:
        start1 = s1.find(substr)
        start2 = s2.find(substr)

        if any(start1 <= e and (start1 + length - 1) >= s for s, e in used_ranges_s1) or \
           any(start2 <= e and (start2 + length - 1) >= s for s, e in used_ranges_s2):
            continue

        selected_substrings.append((substr, length))
        used_ranges_s1.add((start1, start1 + length - 1))
        used_ranges_s2.add((start2, start2 + length - 1))

        if len(selected_substrings) == 3:
            break

    return selected_substrings

# Verification Route
@app.route('/verify_recording', methods=['GET'])
@login_required
def verify_recording():
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_video.webm')

    if not os.path.exists(video_path):
        flash("No recorded video found. Please record again.", "danger")
        return redirect(url_for('video_capture'))  # Redirects to video_capture.html

    detected_pattern = extract_binary_sequence(video_path)

    teacher_attendance = TeachersAttendance.query.filter_by(attID=session["attendance_code"]).first()
    if teacher_attendance is None:

        flash("No Attendance exists for this code ","danger")
        return redirect(url_for('dashboard'))

    original_pattern = teacher_attendance.pattern


    FPS = 30
    DURATION = 2
    TOTAL_FRAMES = FPS * DURATION

    matches = find_longest_common_substrings(detected_pattern, original_pattern)
    total_match_length = sum(length for _, length in matches)
    print("matched frames: " ,total_match_length)

    if total_match_length >= 0.40 * TOTAL_FRAMES:
        flash(f"Attendance verified successfully!{total_match_length}", "success" )


        new_attendance = AttendanceStudents(
            attID=session["attendance_code"],
            username=current_user.username,
            email=current_user.email,
            rollNo=session["roll_number"]
        )
        db.session.add(new_attendance)
        db.session.commit()
        return redirect(url_for('dashboard'))  # Redirects to dashboard after success
    else:
        flash(f"Pattern verification failed! Please try again. Total match length: {total_match_length}", "danger")
        return redirect(url_for('video_capture'))  # Redirects to video_capture.html on failure

if __name__ == "__main__":
    app.run(debug=True, port=5001)
