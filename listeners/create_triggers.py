def create_triggers(cur, table_name):
    create_insert_function_query = f"""
    CREATE OR REPLACE FUNCTION notify_{table_name}_inserts() RETURNS trigger AS $$
    BEGIN
        PERFORM pg_notify('{table_name}_inserts', 'INSERT: ' || row_to_json(NEW)::text);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    cur.execute(create_insert_function_query)

    create_insert_trigger_query = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_trigger WHERE tgname = '{table_name}_inserts_trigger'
        ) THEN
            CREATE TRIGGER {table_name}_inserts_trigger
            AFTER INSERT ON {table_name}
            FOR EACH ROW EXECUTE FUNCTION notify_{table_name}_inserts();
        END IF;
    END;
    $$;
    """
    cur.execute(create_insert_trigger_query)

    create_update_function_query = f"""
    CREATE OR REPLACE FUNCTION notify_{table_name}_updates() RETURNS trigger AS $$
    BEGIN
        PERFORM pg_notify(
            '{table_name}_updates', 
            'UPDATE: ' || json_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW))::text
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    cur.execute(create_update_function_query)

    create_update_trigger_query = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_trigger WHERE tgname = '{table_name}_updates_trigger'
        ) THEN
            CREATE TRIGGER {table_name}_updates_trigger
            AFTER UPDATE ON {table_name}
            FOR EACH ROW EXECUTE FUNCTION notify_{table_name}_updates();
        END IF;
    END;
    $$;
"""
    cur.execute(create_update_trigger_query)
    

    create_delete_function_query = f"""
    CREATE OR REPLACE FUNCTION notify_{table_name}_deletes() RETURNS trigger AS $$
    BEGIN
        PERFORM pg_notify('{table_name}_deletes', 'DELETE: ' || row_to_json(OLD)::text);
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    """
    cur.execute(create_delete_function_query)


    create_delete_trigger_query = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_trigger WHERE tgname = '{table_name}_deletes_trigger'
        ) THEN
            CREATE TRIGGER {table_name}_deletes_trigger
            AFTER DELETE ON {table_name}
            FOR EACH ROW EXECUTE FUNCTION notify_{table_name}_deletes();
        END IF;
    END;
    $$;
    """
    cur.execute(create_delete_trigger_query)
