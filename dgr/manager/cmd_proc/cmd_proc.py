from .reload import reload

Q_GET = (
    "SELECT id, cmd, args "
    "FROM commands "
    "WHERE \"status\" = 'pending' "
    "ORDER BY requested_ts ASC;"
)
U_STATUS = (
    "UPDATE commands "
    "SET \"status\" = %s, last_updated = (now() at time zone 'utc') "
    "WHERE id = %s;"
)

def process_commands(state):
    # Process outstanding commands.
    # Commands may, if they choose, give a notice with nclass command and 
    #   nsubclass being the command
    commands = state.db.querymany(Q_GET)
    if len(commands) == 0:
        return
    for command in commands:
        if command[1] == "reload":
            nstatus = reload(state)
        else:
            nstatus = "fail-unknown"
        state.db.execute(U_STATUS, [nstatus, command[0]])
