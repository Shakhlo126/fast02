from fastapi import FastAPI, HTTPException, Depends
from pydantic import Field, BaseModel
from uuid import UUID
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

app = FastAPI(title='Books API')

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=212)
    author: str = Field(min_length=1, max_length=212)
    description: str = Field(min_length=1, max_length=212)
    price: int = Field(gt=0, lt=1000)

class Tag(BaseModel):
    title: str = Field(min_length=1, max_length=212)

class Category(BaseModel):
    title: str = Field(min_length=1, max_length=212)

class Author(BaseModel):
    name: str = Field(min_length=1, max_length=212)
    surname: str = Field(min_length=1, max_length=212)
    phone_number: int = Field(gt=1 , lt=15)

BOOKS = []


@app.post('/books')
async def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.price = book.price

    db.add(book_model)
    db.commit()

    return book


@app.get('/books')
async def read_books(db: Session = Depends(get_db)):
    return db.query(models.Books).all()


@app.put('/books/{book_id}')
async def read_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'Book with id {book_id} does not exist'
        )
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.price = book.price

    db.add(book_model)
    db.commit()

    return book


@app.delete('/books/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'Book with id {book_id} does not exist'
        )
    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()
    return f'Deleted book with id {book_id}'

#tag
@app.post('/tags')
async def create_tag(tag : Tag, db: Session = Depends(get_db)):
    tag_model = models.Tag
    tag.title = tag.title

    db.add(tag_model)
    db.commit()

    return tag

@app.get('/tags')
async def get_tags(db: Session = Depends(get_db)):
    return db.query(models.Tag).all()

@app.put('/tags/{tag_id}')
async def update_tag(tag_id: int, tag : Tag, db: Session = Depends(get_db)):
    tag_model = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag_model is None:
        raise HTTPException(status_code=404, detail=f'Tag with{tag_id} does not exist')
    tag_model.title = tag.title

    db.add(tag_model)
    db.commit()

    return tag

@app.delete('/tags/{tag_id}')
async def delete_tag(tag_id : int, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == tag_id).first()
    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'Book with id {tag_id} does not exist'
        )
    db.query(models.Books).filter(models.Books.id == tag_id).delete()
    db.commit()
    return f'Deleted book with id {tag_id}'

#Category
@app.post('/categories')
async def create_category(category : Category, db: Session = Depends(get_db)):
    category_model = models.Category
    category.title = category.title

    db.add(category_model)
    db.commit()

    return category

@app.get('/categories')
async def get_category(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@app.put('/categories/{category_id}')
async def update_category(category_id: int, category : Category, db: Session = Depends(get_db)):
    category_model = db.query(models.Tag).filter(models.Category.id == category_id).first()
    if category_model is None:
        raise HTTPException(status_code=404, detail=f'Tag with{category_id} does not exist')
    category_model.title = category.title

    db.add(category_model)
    db.commit()

    return category

@app.delete('/categories/{category_id}')
async def delete_category(category_id : int, db: Session = Depends(get_db)):
    category_model = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'category with id {category_id} does not exist'
        )
    db.query(models.Category).filter(models.Category.id == category_id).delete()
    db.commit()
    return f'Deleted category with id {category_id}'

#author
@app.post('/authors')
async def create_author(author: Author, db: Session = Depends(get_db)):
    author_model = models.Author
    author_model.name = author.name
    author_model.surname = author.surname
    author_model.phone_number = author.phone_number

    db.add(author_model)
    db.commit()

    return author


@app.get('/authors')
async def get_authors(db: Session = Depends(get_db)):
    return db.query(models.Author).all()

@app.put('/authors/{author_id}')
async def put_author(author_id: int, author: Author, db: Session = Depends(get_db)):
    author_model = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'Author with id {author_id} does not exist'
        )


    author_model = models.Author
    author_model.name = author.name
    author_model.surname = author.surname
    author_model.phone_number = author.phone_number

    db.add(author_model)
    db.commit()

    return author

@app.delete('/authors/{author_id}')
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    author_model = db.query(models.Author).filter(models.Author.id).first
    if author_model is None:
        raise HTTPException(status_code=404, detail=f'Author with{author_id} does not exist')
    db.query(models.Author).filter(models.Author.id == author_id).delete
    db.commit()
    return f'Deleted author with id {author_id}'