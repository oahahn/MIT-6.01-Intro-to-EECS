class Library:
    """
    A class used to represent a library.

    Attributes:
        book (str): the title of the book
        books (dict): a list of books
        patron (str): name of a person who uses the library
        date (int): the number of days since the library opened
        dailyFine (float): fine per day a book is overdue
    """
    dailyFine = 0.25
    def __init__(self, books):
        """Takes a list of books and initializes the library."""
        self.shelf = {}
        for book in books:
            self.shelf[book] = (None, None) # (patron, dueDate)

    def checkOut(self, book, patron, date):
        """
        Records the patron and date a book is borrowed. Each book can be kept
        for 7 days before it becomes overdue. It returns None.
        """
        self.shelf[book] = (patron, date+7)
    
    def checkIn(self, book, date):
        """
        Updates the records. 
        
        Returns:
            float: fine if the book is overdue or 0.0 otherwise
        """
        patron, due = self.shelf[book]
        self.shelf[book] = (None, None)
        return max(0.0, (date - due))*self.dailyFine

    def overdueBooks(self, patron, date):
        """Returns a list of overdue books which a patron has on a date"""
        overdue = []
        for book in self.shelf:
            p, d = self.shelf[book]
            if p == patron and date > d:
                overdue.append(book)
        return overdue

class LibraryGrace(Library):
    """
    Extension of the class library with a grace period.

    Attributes:
        grace (int): some number of days after the actual due date before fines 
        start being accumulated
    """
    def __init__(self, grace, books):
        self.grace = grace
        Library.__init__(self, books)
    def checkIn(self, book, date):
        return Library.checkIn(self, book, date - self.grace)

# sample output of the Library class
lib = LibraryGrace(2, ['a', 'b', 'c', 'd', 'e', 'f'])
lib.checkOut('a', 'T', 1)
lib.checkIn('a', 13)
# 0.75

# sample output of the LibraryGrace class
lib = Library(['a', 'b', 'c', 'd', 'e', 'f'])
lib.checkOut('a', 'T', 1)
lib.checkOut('c', 'T', 1)
lib.checkOut('e', 'T', 10)
lib.overdueBooks('T', 13)
# ['a', 'c']
lib.checkIn('a', 13)
# 1.25
lib.checkIn('c', 18)
# 2.50
lib.checkIn('e', 18)
# 0.25