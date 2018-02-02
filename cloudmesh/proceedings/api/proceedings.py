from __future__ import print_function
import os
import yaml
import glob
import os.path
import glob
import yaml
from pprint import pprint
import sys
import re
from cloudmesh.common.util import banner
from cloudmesh.common.util import path_expand


class ProceedingsGit(object):

    def list(self, output="list.txt"):
        """
        curl https://api.github.com/orgs/bigdata-i523/repos?per_page=200 | fgrep ssh_url > list.txt
        :return:
        """
        filename = "tmp.txt"
        os.system(
            "curl https://api.github.com/orgs/bigdata-i523/repos?per_page=200 -o {filename}".format(filename=filename))
        with open(filename, 'r') as f:
            content = f.read()
        lines = content.split('\n')
        content = []

        for line in lines:
            if ("ssh_url" in line and "/hid" in line):
                content.append(line)
        content.sort()
        t = '\n'.join(content)

        text_file = open(output, "w")
        text_file.write(t)
        text_file.close()


class Proceedings(object):
    def __init__(self, directory="~/github/bigdata-i523"):
        self.set_home(directory)


    def set_home(self, directory):
        self.home = path_expand(directory)

    def execute(self, hid, command, base='paper1', kind='paper1'):
        banner(hid + ": " + command)
        commandline = "cd {home}/{hid}/{kind}; {command} > p.log".format(home=self.home,
                                                                 command=command,
                                                                 hid=hid,
                                                                 base=base,
                                                                 kind=kind)
        try:
            os.system(commandline)
        except Exception as e:
            print(e)
            print("ERROR: can not", command, hid)

    def generate_pdf(self, hid, base='paper1', kind='paper1'):
        self.execute("make", hid, base=base, kind=kind)

    def view_pdf(self, hid, base='paper1', kind='paper1'):
        self.execute("make view", hid, base=base, kind=kind)

    def clean_pdf(self, hid, base='paper1', kind='paper1'):
        self.execute("make clean", hid, base=base, kind=kind)

    def read_git_list(self, filename='list.txt'):
        gits = []
        with open(filename, 'r') as f:
            for line in f:
                url = line.split('"')[3]
                gits.append(url)
        return gits

    def read_hid_list(self, filename='list.txt'):
        hids = []
        gits = self.read_git_list(filename)
        for git in gits:
            rest, hid = git.split("/")
            hid = hid.replace(".git", "")
            hids.append(hid)
        return hids

    def get_hids_from_git(self):
        """ returns the hids from git"""
        return []

    def get_hids_from_list(self, parameter):
        """use cloudmesh Parameter to generate a list form abreviated list string"""
        """example hid[100-110,116,201-210,301-305]"""
        return

    def clean(self):
        hids = self.read_hid_list(filename='list.txt')
        for hid in hids:
            os.system("rm -rf {home}/{hid}".format(home=self.home, hid=hid))

    def clone(self, filename='list.txt'):
        """ clones all hid dirs int .."""
        """returns all hids that have an issue"""
        hids = self.read_git_list(filename=filename)
        for hid in hids:
            if "/hid" in hid:
                os.system("cd {home}; git clone {hid}".format(hid=hid, home=self.home))

    def pull(self, filename='list.txt'):
        """does a git pull in all hid dirs in .."""
        """returns all hid the have an issue"""
        hids = self.read_hid_list(filename=filename)
        # print(hids)
        for hid in hids:
            print(hid)
            os.system("cd {home}/{hid}; git pull ".format(hid=hid, home=self.home))

    def status(self, filename='list.txt'):
        """does a git status in all hid dirs in .."""
        """returns all hid the have an issue"""
        hids = self.read_hid_list(filename=filename)
        # print(hids)
        for hid in hids:
            print(hid)
            os.system("cd {home}/{hid}; git status ".format(hid=hid, home=self.home))

    def commit(self, filename='list.txt', msg="update"):
        """does a git pull in all hid dirs in .."""
        """returns all hid the have an issue"""
        hids = self.read_hid_list(filename=filename)
        # print(hids)
        for hid in hids:
            print(hid)
            os.system('cd {home}/{hid}; git commit -m "{msg}" . '.format(hid=hid, msg=msg, home=self.home))

    def push(self, filename='list.txt'):
        """does a git pull in all hid dirs in .."""
        """returns all hid the have an issue"""
        hids = self.read_hid_list(filename=filename)
        print(hids)
        for hid in hids:
            print(hid)
            os.system('cd {home}/{hid}; git push'.format(hid=hid, home=self.home))

    def set_license(self):
        """put the license in each directory if it is missing"""
        """ this is not working"""
        self.read_hid_list()
        for line in content:
            directory = line.split('/')[4].split(".")[0]
            if directory.startswith('hid'):
                print(directory)
                # os.system("cp proceedings/LICENSE " + directory)
                # os.system('cd ' + directory + ';  git commit -m "add License" LICENSE; git push')

    def get_file(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except Exception as e:
            print(e)
            content = None
        return content

    def readme(self, hid):
        filename = "{home}/{hid}/README.yml".format(hid=hid, home=self.home)
        content = None
        try:

            if os.path.isfile(filename):
                content = self.get_file(filename)
                # content = yaml.load(content)
                # print (content)
                # content = self.extract_yaml_text(content)
        except Exception as e:
            pass
        return content

    def attribute(self, hid, name):
        if hid is not None:
            s = self.readme(hid)
            if s is None:
                return None
            try:
                data = yaml.load(s)
            except Exception as e:
                print(e)
                data = None

            if data is None:
                return None
            return data[name]

        else:
            ok = {}
            missing = []
            dirs = glob.glob('{home}/hid*'.format(home=self.home))
            for directory in dirs:
                hid = directory.replace("{home}/".format(home=self.home), "")
                print(hid)
                try:
                    filename = directory + '/README.yml'
                    if os.path.isfile(filename):
                        data = self.attribute(hid, name)
                        data['dir'] = hid
                        #print(data)
                        if data is None:
                            missing.append("{hid}, owner data is missing in README.yml".format(hid=hid))
                        else:
                            ok[hid] = data
                except:
                    data['dir'] = hid
                    data['hid'] = 'None'
                    data['type'] = 'None'
                    data['chapter'] = 'None'
                    data['author'] = 'None'
                    data['title'] = 'None'

            return ok, missing
