from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
import re
from database import SessionLocal, engine, Base
import models
import schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marriage Matchmaking App")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Email validation function
def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

# Create user endpoint
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Validate email
    if not validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    db_user = models.User(
        name=user.name,
        age=user.age,
        gender=user.gender,
        email=user.email,
        city=user.city,
        interests=user.interests
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read all users endpoint
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# Read user by ID endpoint
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update user endpoint
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    # Find the user
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate email if being updated
    if user.email is not None:
        if not validate_email(user.email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        # Check if new email already exists (only if email is being changed)
        if user.email != db_user.email:
            existing_email = db.query(models.User).filter(models.User.email == user.email).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="Email already registered")

    # Update user attributes
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete user endpoint
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Find the user
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Find matches endpoint
@app.get("/users/{user_id}/matches", response_model=List[schemas.User])
def find_matches(
    user_id: int,
    min_compatibility: float = 0.3,  # Minimum compatibility score (30%)
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Find the user
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all users of opposite gender
    opposite_gender = "male" if user.gender.lower() == "female" else "female"
    potential_matches = db.query(models.User).filter(
        models.User.gender.ilike(opposite_gender),
        models.User.id != user_id
    ).all()

    # Calculate compatibility scores
    matches_with_scores = []
    for potential_match in potential_matches:
        # Calculate compatibility based on multiple factors
        compatibility_score = 0.0

        # 1. Age compatibility (higher score for similar ages, max 0.3)
        age_diff = abs(user.age - potential_match.age)
        if age_diff <= 5:
            compatibility_score += 0.3
        elif age_diff <= 10:
            compatibility_score += 0.2
        elif age_diff <= 15:
            compatibility_score += 0.1

        # 2. Location compatibility (same city, 0.2)
        if user.city.lower() == potential_match.city.lower():
            compatibility_score += 0.2

        # 3. Interests compatibility (shared interests, max 0.5)
        user_interests = set(user.interests.lower().split(','))
        match_interests = set(potential_match.interests.lower().split(','))

        # Calculate Jaccard similarity for interests
        if user_interests and match_interests:
            intersection = user_interests.intersection(match_interests)
            union = user_interests.union(match_interests)
            interest_similarity = len(intersection) / len(union) if union else 0
            compatibility_score += interest_similarity * 0.5

        # Add to matches if above minimum compatibility threshold
        if compatibility_score >= min_compatibility:
            matches_with_scores.append((potential_match, compatibility_score))

    # Sort by compatibility score (descending) and limit results
    matches_with_scores.sort(key=lambda x: x[1], reverse=True)
    top_matches = [match[0] for match in matches_with_scores[:limit]]

    return top_matches