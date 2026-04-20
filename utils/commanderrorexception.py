class CommandErrorException(Exception):
    """Exception for failed Interaction to reset the cooldown"""

    def __init__(self,user,guild,commandname,cooldown):
        self.user = user
        self.guild = guild
        self.command_name = commandname
        self.cooldown = cooldown

        super().__init__(self.user,self.guild,self.command_name)
#####################################################################################################
    def __str__(self):
        return self.cooldown.reset()