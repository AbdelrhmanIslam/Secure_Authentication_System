import bcrypt

def hash_password(plain_text_password):
    # purpose: takes the user's raw password string and returns a hashed version
    # that is safe to store in the database — never store passwords as plain text
    
    # encode the string to bytes because bcrypt requires byte input
    password_bytes = plain_text_password.encode('utf-8')
    
    # generate a unique salt for this user to defend against rainbow table attacks
    salt = bcrypt.gensalt()
    
    # combine the password and salt, then hash them together
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # decode the byte hash back to a string so it can be cleanly saved in our database column
    return hashed_bytes.decode('utf-8')

def check_password(plain_text_password, stored_hash):
    # purpose: compares a login attempt against the stored hash
    # returns True if they match, False if not
    
    # encode the incoming login attempt into bytes for comparison
    attempt_bytes = plain_text_password.encode('utf-8')
    
    # encode the string hash from the database back into bytes for the bcrypt function
    hash_bytes = stored_hash.encode('utf-8')
    
    # check if the login attempt hashes to the same value as the stored hash
    return bcrypt.checkpw(attempt_bytes, hash_bytes)