from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.community.api.community import Community, Repos, CommunityGit
from pprint import pprint
from cloudmesh.common.Printer import Printer
import os

class CommunityCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_community(self, args, arguments):
        """
        ::

          Usage:
                community git list
                community clone [git=BASE] [HIDS]
                community pull
                community status
                community push
                community commit MESSAGE
                community check [HIDS]
                community create
                community delete
                community clean
                community list ATTRIBUTE [HID]
                community pdf HID KIND make
                community pdf HID KIND view
                community pdf HID KIND clean
                community pdf HID KIND ls
                community pdf HID KIND cat FILE


          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        # pprint(arguments)

        if arguments.git and arguments.list:

            p = CommunityGit()
            print ("bbb")
            repos = Repos()
            print ("aa")
            pprint (repos.config)
            org = repos.config['github']['org']
            print ("aa",org)
            p.list(org=org)
            return

        p = Community()
        c  = p.read_git_list(filename='list.txt')

        if arguments.clone:
            hids = p.clone(filename='list.txt')

        elif arguments.commit:
            msg = arguments.MESSAGE
            p.commit(filename='list.txt', msg=msg)
            p.push(filename='list.txt')

        elif arguments.pull:
            hids = p.pull(filename='list.txt')

        elif arguments.push:
            hids = p.push(filename='list.txt')

        elif arguments.status:
            hids = p.status(filename='list.txt')

        elif arguments.list and arguments.hids:
            print(p.read_hid_list(filename='list.txt'))

        elif arguments.list and arguments.ATTRIBUTE:
            hid = arguments.HID
            if hid is not None:
                # print(p.readme(hid))
                ok= p.attribute(hid, arguments.ATTRIBUTE)
                # print (ok)
                # print()
                # print ("Owner Data Missing")
                # print ("\n".join(missing))
            else:
                ok, missing = p.attribute(None, arguments.ATTRIBUTE)
                #pprint (ok)
                #pprint (missing)
                if arguments.ATTRIBUTE == 'owner':
                    print(Printer.write(ok, order=['hid', 'name', 'url']))
                elif arguments.ATTRIBUTE.startswith('paper'):
                    print(Printer.write(ok, order=['dir', 'hid', 'exclude', 'chapter', 'author', 'title']))
                elif arguments.ATTRIBUTE.startswith('project'):
                    print(Printer.write(ok, order=['dir', 'hid', 'type', 'exclude', 'chapter', 'author', 'title']))

        elif arguments.pdf and arguments.make:

            hid = arguments.HID
            kind = arguments.KIND


            if hid.lower() == "all":

                dirs = p.read_hid_list(filename='list.txt')

                for directory in dirs:
                    # print(directory)
                    if os.path.exists("{home}/{directory}".format(home=p.home,directory=directory)) and \
                       os.path.exists("{home}/{directory}/{kind}/report.tex".format(home=p.home,kind=kind,directory=directory)):
                        # print ("compile")
                        p.execute(directory, "make", base=kind, kind=kind)

            else:
                p.execute(hid, "make", base=kind, kind=kind)

        elif arguments.pdf and arguments.view:

            hid = arguments.HID
            kind = arguments.KIND

            p.execute(hid, "make view", base=kind, kind=kind)

        elif arguments.pdf and arguments.clean:

            hid = arguments.HID
            kind = arguments.KIND

            if hid.lower() == "all":

                dirs = p.read_hid_list(filename='list.txt')

                for directory in dirs:
                    if os.path.isfile("{home}/{directory}".format(home=p.home, directory=directory)):
                        p.execute(directory, "make clean", base=kind, kind=kind)

            else:
                p.execute(hid, "make clean", base=kind, kind=kind)

        elif arguments.pdf and arguments.ls:

            hid = arguments.HID
            kind = arguments.KIND

            p.execute(hid, "ls", base=kind, kind=kind)

        elif arguments.pdf and arguments.cat:

            hid = arguments.HID
            kind = arguments.KIND
            file = arguments.FILE

            p.execute(hid, "cat {file}".format(file=file), base=kind, kind=kind)


        elif arguments.clean:
            p.clean()

