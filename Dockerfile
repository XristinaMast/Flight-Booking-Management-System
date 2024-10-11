# Χρήση της επίσημης εικόνας Python ως βάση
FROM python:3.9

# Ορισμός του working directory
WORKDIR /app

# Αντιγραφή των αρχείων στον Docker Container
COPY . .

# Προετοιμάσια για εγκατάσταση Python
RUN apt-get update
RUN pip install --no-cache-dir --upgrade pip

# Εγκατάσταση των dependencies που χρειάζεται η python
RUN pip install -r requirements.txt

# Εκκίνηση της εφαρμογής
CMD ["python", "code.py"]
