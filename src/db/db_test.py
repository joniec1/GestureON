from supabase_client import supabase

def test_insert_user():
    data = {
        "nickname": "test_user"
    }

    response = supabase.table("users").insert(data).execute()
    print(response)

if __name__ == "__main__":
    test_insert_user()