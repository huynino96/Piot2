import bcrypt

'''
This class is for hashing users' password using bcrypt algorithm
'''


class Hasher:
    @staticmethod
    def hash(pwd):
        # Password must be in bytes before hashing
        pwd = str.encode(pwd)
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd, salt)    # bcrypt.hashpw returns bytes => convert to string before returning

    @staticmethod
    def if_matched(pwd, hashed):
        pwd = str.encode(pwd)   # Turn string to bytes to use checkpw function
        hashed = str.encode(hashed) # Turn string to bytes to use checkpw function
        return bcrypt.checkpw(pwd, hashed)


if __name__ == "__main__":
    pwd = "weAreOne"
    hashed = Hasher.hash(pwd)
    print(hashed)

    if Hasher.if_matched(pwd, hashed):
        print("Matched {} and {}".format(pwd, hashed))
    else:
        print("Does not match")
