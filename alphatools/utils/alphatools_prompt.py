from cmd import Cmd
 
class AlphaToolsCliPrompt(Cmd):
    def do_exit(self, inp):
        print("Bye")
        return True
     
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
        
    do_EOF = do_exit
    help_EOF = help_exit


if __name__ == '__main__':
    AlphaToolsCliPrompt().cmdloop()