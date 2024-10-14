import os
from fastapi import FastAPI, Depends, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from evaluation import (
    check_for_harmful_content,
    evaluate_length,
    evaluate_options,
    evaluate_readability,
)
from summary import summarize_text
from bullet_points import extract_bullet_points
from generate_story import generate_story
from models import FavoriteStory, Story, User, SessionLocal
from auth import get_password_hash, authenticate_user
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

SECRET_KEY = os.getenv("SECRET_KEY", "basy7ca8qjw9xnjs9xskijix2w830800ih")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS Middleware to allow the frontend to make requests to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

load_dotenv()
db_path = os.getenv("DB_PATH")

# Create the full SQLite database URL
DATABASE_URL = f"sqlite:///{db_path}"

# Configure the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency: get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example route to check database connectivity
@app.get("/check_db")
def check_db():
    return {"db_path": db_path}


class UserCreate(BaseModel):
    username: str
    password: str
    favorites_summary: str
    saved_stories: str


@app.post("/register")
async def register(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return JSONResponse(content={"message": "Username already registered"}, status_code=200)


    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        hashed_password=hashed_password,
        favorite_stories=[],
        saved_stories=[],
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(content={"message": "User registered successfully"}, status_code=200)



@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, username, password)
    request.session["username"] = username

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return RedirectResponse(url="/home", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    story = request.session.get("story")
    username = request.session.get("username")
    return templates.TemplateResponse("home.html", {"request": request, "story": story, "username": username})


@app.post("/generate-story", response_class=HTMLResponse)
async def generate_story_endpoint(
    request: Request,
    protagonistName: str = Form(...),
    protagonistGender: str = Form(...),
    friendName: str = Form(None),
    friendGender: str = Form(None),
    storyTheme: str = Form(...),
    ageGroup: str = Form(None),
    educationalContent: str = Form(None),
    storyDescription: str = Form(None),
    storyLength: str = Form(None),
    useFavorites: bool = Form(False),
    db: Session = Depends(get_db),
):
    data = {
        "protagonistName": protagonistName,
        "protagonistGender": protagonistGender,
        "friendName": friendName,
        "friendGender": friendGender,
        "storyTheme": storyTheme,
        "ageGroup": ageGroup,
        "educationalContent": educationalContent,
        "storyDescription": storyDescription,
        "storyLength": storyLength,
    }

    # Retrieve bullet points from favorite stories if the checkbox is checked
    bullet_points = []
    if useFavorites:
        username = request.session.get("username")
        user = db.query(User).filter(User.username == username).first()
        if user:
            favorites = db.query(FavoriteStory).filter(FavoriteStory.user_id == user.id).all()
            for favorite in favorites:
                bullet_points.extend(favorite.bullet_points)

    # Generate the story
    story_content = generate_story(data, bullet_points)

    print(request.session.get("username"))
    user = (
        db.query(User).filter(User.username == request.session.get("username")).first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create and save the story to the database
    new_story = Story(
        user_id=user.id,
        content=story_content,
        protagonist_name=protagonistName,
        protagonist_gender=protagonistGender,
        friend_name=friendName,
        friend_gender=friendGender,
        story_theme=storyTheme,
        age_group=ageGroup,
        educational_content=educationalContent,
        story_description=storyDescription,
        story_length=storyLength,
    )
    db.add(new_story)
    db.commit()

    # Store the story and data in the session for evaluation
    request.session["story"] = story_content
    request.session["data"] = data

    if "evaluations" in request.session:
        del request.session["evaluations"]

    return templates.TemplateResponse(
        "home.html", {"request": request, "story": story_content}
    )


"""
@app.get("/story-evaluation", response_class=HTMLResponse)
async def story_evaluation_page(request: Request):
    story = request.session.get("story")
    data = request.session.get("data")
    evaluations = request.session.get("evaluations")

    if not story or not data:
        return RedirectResponse(url="/home")

    if not evaluations:
        # Running evaluations
        options_evaluation = evaluate_options(story, data)
        length_evaluation = evaluate_length(story, data["storyLength"])
        readability_evaluation = evaluate_readability(story, data["ageGroup"])
        harmful_content_evaluation = check_for_harmful_content(story, data["ageGroup"])
        evaluations = {
            "story": story,
            "options_evaluation": options_evaluation,
            "length_evaluation": length_evaluation,
            "readability_evaluation": readability_evaluation,
            "harmful_content_evaluation": harmful_content_evaluation,
        }

        # Storing evaluations in the session
        request.session["evaluations"] = evaluations
    else:
        evaluations = evaluations

    return templates.TemplateResponse(
        "evaluation.html", {"request": request, "evaluations": evaluations}
    )
"""

class FavoriteStory_(BaseModel):
    storyText: str
    isFavorited: bool


@app.post("/save-favorite")
async def save_favorite(
    favorite_story: FavoriteStory_, request: Request, db: Session = Depends(get_db)
):
    try:
        user = (
            db.query(User)
            .filter(User.username == request.session.get("username"))
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        summary = summarize_text(favorite_story.storyText)
        bullet_points = extract_bullet_points(favorite_story.storyText)
        
        new_favorite_story = FavoriteStory(
            story_content=favorite_story.storyText,
            summary_text=summary,
            bullet_points=bullet_points,
            user_id=user.id  
        )
        user.favorite_stories.append(new_favorite_story)

        db.add(new_favorite_story)
        db.commit()
        return {"message": "Favorite saved", "summary": summary, "bullet_points": bullet_points}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/remove-favorite")
async def remove_favorite(story_data: dict, request: Request, db: Session = Depends(get_db)):
    try:
        user = (
            db.query(User)
            .filter(User.username == request.session.get("username"))
            .first()
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Find the story in the user's favorite stories
        story_to_remove = (
            db.query(FavoriteStory)
            .filter(FavoriteStory.user_id == user.id, FavoriteStory.story_content == story_data["storyText"])
            .first()
        )

        if story_to_remove:
            db.delete(story_to_remove)
            db.commit()
            return {"message": "Favorite removed"}
        else:
            return {"message": "Story not found in favorites"}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/past-stories", response_class=HTMLResponse)
async def past_stories_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == request.session.get("username")).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Retrieve all stories for the user
        stories = db.query(Story).filter(Story.user_id == user.id).all()
        if stories is None:
            stories = []
        
        return templates.TemplateResponse("stories.html", {"request": request, "stories": stories})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/favorites", response_class=HTMLResponse)
async def favorites_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == request.session.get("username")).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Retrieve all favorite stories for the user
        favorites = db.query(FavoriteStory).filter(FavoriteStory.user_id == user.id).all()
        
        return templates.TemplateResponse("favorites.html", {"request": request, "favorites": favorites})
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")