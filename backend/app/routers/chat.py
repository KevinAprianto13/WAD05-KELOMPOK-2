from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from typing import List

from app.db.session import get_db
from app.models.models import User, ChatMessage, UserRole
from app.schemas.schemas import ChatMessageCreate, ChatMessageOut, ChatSessionOut, UserOut
from app.core.deps import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatMessageOut)
def send_message(
    data: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    receiver_id = data.receiver_id
    if current_user.role == "customer":
        if not receiver_id:
            # find an admin
            admin = db.query(User).filter(User.role == "admin").first()
            if not admin:
                raise HTTPException(status_code=400, detail="No admin available to receive message.")
            receiver_id = admin.id
    
    msg = ChatMessage(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=data.content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

@router.get("/sessions", response_model=List[ChatSessionOut])
def get_chat_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    messages = db.query(ChatMessage).filter(
        or_(ChatMessage.sender_id == current_user.id, ChatMessage.receiver_id == current_user.id)
    ).order_by(desc(ChatMessage.created_at)).all()
    
    sessions = {}
    for msg in messages:
        other_user_id = msg.sender_id if msg.sender_id != current_user.id else msg.receiver_id
        if other_user_id not in sessions:
            other_user = db.query(User).get(other_user_id)
            if other_user:
                unread_count = db.query(ChatMessage).filter(
                    ChatMessage.sender_id == other_user_id,
                    ChatMessage.receiver_id == current_user.id,
                    ChatMessage.is_read == False
                ).count()
                
                sessions[other_user_id] = {
                    "user": other_user,
                    "last_message": msg,
                    "unread_count": unread_count
                }
                
    return list(sessions.values())


@router.get("/{user_id}", response_model=List[ChatMessageOut])
def get_messages_with_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "customer" and user_id == 0:
        admin = db.query(User).filter(User.role == "admin").first()
        if admin:
            user_id = admin.id
        else:
            return []
    unread_msgs = db.query(ChatMessage).filter(
        ChatMessage.sender_id == user_id,
        ChatMessage.receiver_id == current_user.id,
        ChatMessage.is_read == False
    ).all()
    
    for msg in unread_msgs:
        msg.is_read = True
    if unread_msgs:
        db.commit()

    messages = db.query(ChatMessage).filter(
        or_(
            and_(ChatMessage.sender_id == current_user.id, ChatMessage.receiver_id == user_id),
            and_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == current_user.id)
        )
    ).order_by(ChatMessage.created_at).all()
    
    return messages
