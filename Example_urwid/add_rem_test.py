#!/usr/bin/env python


import urwid
from enum import Enum
from urwidtrees.tree import SimpleTree
from urwidtrees.decoration import CollapsibleArrowTree
from urwidtrees.widgets import TreeBox


class CustomTreeBox(TreeBox):
    def __init__(self, parent=None, *args, **keywords):
        super().__init__(*args, **keywords)
        self.parent = parent
        # -----------------------------------------------------------
        # expand/collapse where needed
        # tree_nodes = load_tree_data(filename=self.parent.filename)
        # for tree_node in tree_nodes:
        #     # -------------------------------------------------------
        #     tree_node_path = tree_node["tree_path"]
        #     expanded = tree_node["expanded"]
        #     # -------------------------------------------------------
        #     node = self.get_node_tuple(tree_node_path)
        #     if node is None:
        #         continue
        #     pos = node[1]
        #     if expanded == 'True':
        #         self._tree.expand(pos)
        #     else:
        #         self._tree.collapse(pos)
        return

    def delete_node(self):
        # -----------------------------------------------------------
        message = """
        WARNING:
        This will permanently delete all associated nodes.
        """
        # -----------------------------------------------------------
        dialog = DialogTextYesNo(
                message=message,
                parent=self.parent.frame,
                caption="Delete Node?"
            )
        dialog.loop.run()
        result = dialog.result
        self.parent.loop.screen.clear()
        # -----------------------------------------------------------
        if result is DialogResult.NO:
            return
        # -----------------------------------------------------------
        (_, focused_pos) = self.get_focus()
        tree_list = self._tree._tree._treelist
        index = self.get_node_index(tree_list=tree_list)
        parent_pos = self._tree.parent_position(focused_pos)
        focused_tuple = index[focused_pos]["node"]
        if parent_pos is None:  # don't delete the root
            return
        else:
            parent_tuple = index[parent_pos]['node']
            (_, i) = find_child(
                    child=focused_tuple[0].text, child_list=parent_tuple[1])
        child_to_remove = parent_tuple[1][i]
        parent_tuple[1].remove(child_to_remove)
        # -----------------------------------------------------------
        if len(parent_tuple[1]) == 0:
            parent_tuple = self.rebuild_tuple(parent_tuple, parent_pos)
        # -----------------------------------------------------------
        self.refresh()
        # -----------------------------------------------------------
        # self.save()
        # -----------------------------------------------------------
        return

    def edit_node_text(self):
        # -----------------------------------------------------------
        caption = "Edit Node"
        dialog = DialogEditBoxOKCancel(
                parent=self.parent.frame, caption=caption)
        # -----------------------------------------------------------
        (w, focused_pos) = self.get_focus()
        focused_widget = self._tree[focused_pos]
        dialog.edit.set_edit_text(focused_widget.text)
        # -----------------------------------------------------------
        dialog.loop.run()
        result = dialog.result
        self.parent.loop.screen.clear()
        if result is DialogResult.CANCEL:
            return
        # -----------------------------------------------------------
        focused_widget.text = dialog.edit.text
        # -----------------------------------------------------------
        self.refresh()
        # self.save()
        # -----------------------------------------------------------
        return

    def get_node_index(
                self,
                tree_list=None,
                d={},
                parent=None,
                depth=1
            ):
        i = 0
        for node in tree_list:
            (w, children) = node
            text = w.text
            type(text)
            if parent is None:
                pos = (i,)
            else:
                if len(parent) < depth:
                    pos = parent + (i,)
                else:
                    pos_l = list(parent)
                    pos_l[-1] = i
                    pos = tuple(pos_l)
            d[pos] = {}
            d[pos]["node"] = node
            i += 1
            parent = pos
            if children:
                self.get_node_index(
                        tree_list=children,
                        d=d,
                        parent=parent,
                        depth=depth + 1,
                    )
        return d

    def get_node_tuple(self, path):
        # -----------------------------------------------------------------
        for pos in self._tree.positions():
            widget = self._tree[pos]
            tree_path = self.get_tree_path(widget, pos)
            if tree_path == path:
                return (widget, pos)
        # -----------------------------------------------------------------
        return None

    def get_pos_list(
            self,
            tree_list=None,
            pos_list=None,
            parent=None,
            depth=1):
        i = 0
        for node in tree_list:
            (w, children) = node
            if parent is None:
                pos = (i,)
            else:
                if len(parent) < depth:
                    pos = parent + (i,)
                else:
                    pos_l = list(parent)
                    pos_l[-1] = i
                    pos = tuple(pos_l)
            pos_list.append(pos)
            i += 1
            parent = pos
            if children:
                self.get_pos_list(
                        tree_list=children,
                        pos_list=pos_list,
                        parent=parent,
                        depth=depth + 1,
                    )
        return pos_list

    def get_tree_nodes(self, tree=None):
        '''pass in CollapsibleArrowTree'''
        # -----------------------------------------------------------
        nodes = []
        # -----------------------------------------------------------
        if tree is None:
            tree = self._tree
        tree_list = tree._tree._treelist
        pos_list = self.get_pos_list(tree_list=tree_list, pos_list=[])
        # -----------------------------------------------------------
        for pos in pos_list:
            node = {}
            w = tree[pos]
            tree_path = self.get_tree_path(w, pos)
            node["tree_path"] = tree_path
            collapsed = tree.is_collapsed(pos)
            if collapsed:
                node["expanded"] = "False"
            else:
                node["expanded"] = "True"
            nodes.append(node)
        # -----------------------------------------------------------
        return nodes

    def get_tree_path(self, widget=None, pos=None):
        # -----------------------------------------------------------------
        tree_path = widget.text
        # -----------------------------------------------------------------
        while self._tree.parent_position(pos) is not None:
            pos = self._tree.parent_position(pos)
            widget = self._tree[pos]
            tree_path = widget.text + "\\" + tree_path
        # -----------------------------------------------------------------
        return tree_path

    def keypress(self, size, key):
        key = self.__super.keypress(size, key)
        if key in [' ', "enter"]:
            self.toggle_expand()
            return None
        elif key in ['n']:
            self.new_node()
            return None
        elif key in ['d']:
            self.delete_node()
            return None
        elif key in ['e']:
            self.edit_node_text()
            return None
        elif key in ['t']:
            # self.test_function()
            return None
        return key

    def new_node(self):
        # -----------------------------------------------------------
        caption = "New Node"
        dialog = DialogEditBoxOKCancel(
                parent=self.parent.frame, caption=caption)
        dialog.loop.run()
        result = dialog.result
        self.parent.loop.screen.clear()
        if result is DialogResult.CANCEL:
            return
        # -----------------------------------------------------------
        tree_list = self._tree._tree._treelist
        node_index = self.get_node_index(tree_list=tree_list)
        (_, focused_pos) = self.get_focus()
        focused_tuple = node_index[focused_pos]['node']
        # -----------------------------------------------------------
        if focused_tuple[1] is None:
            focused_tuple = self.rebuild_tuple(focused_tuple, focused_pos)
        # -----------------------------------------------------------
        new_tuple = (FocusableText(dialog.edit.text), None)
        focused_tuple[1].append(new_tuple)
        self.refresh()
        # self.save()
        # -----------------------------------------------------------
        return

    def reassign_tuple(self, rebuilt_tuple=None, parent_pos=None):
        tree_list = self._tree._tree._treelist
        node_index = self.get_node_index(tree_list=tree_list)
        parent_tuple = node_index[parent_pos]['node']
        _, i = find_child(
                child=rebuilt_tuple[0].text, child_list=parent_tuple[1])
        parent_tuple[1][i] = rebuilt_tuple
        return

    def rebuild_tuple(self, t, pos):
        # -----------------------------------------------------------
        t = list(t)
        if t[1] is None:
            t[1] = []
        else:
            t[1] = None
        t = tuple(t)
        # -----------------------------------------------------------
        tree_list = self._tree._tree._treelist
        # -----------------------------------------------------------
        parent_pos = self._tree.parent_position(pos)
        if parent_pos is None:
            tree_list[0] = t
        else:
            self.reassign_tuple(t, parent_pos)
        # -----------------------------------------------------------
        return t

    def toggle_expand(self):
        w, pos = self.get_focus()
        self._tree.toggle_collapsed(pos)
        self._walker.clear_cache()
        self.refresh()
        # self.save()

    def test_function(self):
        # # -----------------------------------------------------------
        # (_, focused_pos) = self.get_focus()
        # tree_list = self._tree._tree._treelist
        # index = self.get_node_index(tree_list=tree_list)
        # parent_pos = self._tree.parent_position(focused_pos)
        # focused_tuple = index[focused_pos]["node"]
        # if parent_pos is None:  # don't delete the root
        #     return
        # else:
        #     parent_tuple = index[parent_pos]['node']
        #     (_, i) = find_child(
        #             child=focused_tuple[0].text, child_list=parent_tuple[1])
        # child_to_remove = parent_tuple[1][i]
        # parent_tuple[1].remove(child_to_remove)
        # # -----------------------------------------------------------
        # if len(parent_tuple[1]) == 0:
        #     parent_tuple = self.rebuild_tuple(parent_tuple, parent_pos)
        # # -----------------------------------------------------------
        # self.refresh()
        # # -----------------------------------------------------------
        # # self.save()
        # # -----------------------------------------------------------
        return


class DialogEditBoxOKCancel():
    def __init__(self, parent=None, caption=None, *args, **keywords):
        # -----------------------------------------------------------
        self.parent = parent
        self.caption = caption
        # -----------------------------------------------------------
        self.edit = urwid.Edit()
        body = urwid.ListBox(urwid.SimpleListWalker([self.edit]))
        body = urwid.AttrWrap(body, 'body', 'focus')
        body = urwid.LineBox(body)
        body = urwid.AttrMap(body, "border", "border")
        self.frame = urwid.Frame(body)
        overlay = urwid.Overlay(
                top_w=self.frame,
                bottom_w=self.parent,
                align="center",
                width=30,
                valign="middle",
                height=7,
            )
        overlay = urwid.AttrMap(overlay, 'body')
        self.loop = urwid.MainLoop(
            widget=overlay,
            palette=self.get_palette(),
            unhandled_input=self.unhandled_input)
        # -----------------------------------------------------------
        ok_button = urwid.Button("OK", self.button_ok)
        ok_button = urwid.AttrMap(ok_button, "body", "focus")
        cancel_button = urwid.Button("CANCEL", self.button_cancel)
        cancel_button = urwid.AttrMap(cancel_button, "body", "focus")
        buttons = [ok_button, cancel_button]
        button_grid = urwid.GridFlow(buttons, 10, 3, 1, "center")
        caption = urwid.Text(self.caption)
        caption = urwid.AttrMap(caption, "header", "")
        self.frame.header = urwid.Pile([caption])
        button_grid = urwid.AttrMap(button_grid, "header", "")
        divider = urwid.AttrMap(urwid.Divider(), "header", "header")
        self.frame.footer = urwid.Pile(
                [divider, button_grid, divider], focus_item=1)
        # -----------------------------------------------------------
        return

    def button_cancel(self, data):
        self.result = DialogResult.CANCEL
        raise urwid.ExitMainLoop()
        return

    def button_ok(self, data):
        self.result = DialogResult.OK
        raise urwid.ExitMainLoop()
        return

    def get_palette(self):
        palette = [
            ("body", "black", "light gray"),
            ("current_node", "dark red", "light gray"),
            ("focus", "light gray", "dark blue", "standout"),
            ("reveal_focus", "black", "dark cyan", "standout"),
            ("column_headers", "dark red", "light gray"),
            ("header", "light red", "black"),
            ('border', 'light red', 'black'),
        ]
        return palette

    def unhandled_input(self, key):
        if key == 'tab':
            button_grid = self.frame.footer[1]
            if self.frame.get_focus() == 'body':
                self.frame.set_focus('footer')
                button_grid.focus_position = 0
                return
            elif self.frame.get_focus() == 'footer':
                if button_grid.focus_position == 0:
                    button_grid.focus_position = 1
                    return
                else:
                    self.frame.set_focus("body")
                    return
            else:
                pass
        return


class DialogTextYesNo():
    def __init__(
            self,
            parent=None,
            caption=None,
            message=None,
            *args,
            **keywords):
        # -----------------------------------------------------------
        self.parent = parent
        self.caption = caption
        self.text_widget = urwid.Text(message)
        # -----------------------------------------------------------
        body = urwid.ListBox(urwid.SimpleListWalker([self.text_widget]))
        body = urwid.AttrWrap(body, 'focus', 'focus')
        body = urwid.LineBox(body)
        body = urwid.AttrMap(body, "border", "border")
        self.frame = urwid.Frame(body)
        overlay = urwid.Overlay(
                top_w=self.frame,
                bottom_w=self.parent,
                align="center",
                width=70,
                valign="middle",
                height=10,
            )
        self.loop = urwid.MainLoop(
            widget=overlay,
            palette=self.get_palette(),
            unhandled_input=self.unhandled_input)
        # -----------------------------------------------------------
        ok_button = urwid.Button("YES", self.button_yes)
        ok_button = urwid.AttrMap(ok_button, "body", "focus")
        cancel_button = urwid.Button("NO", self.button_no)
        cancel_button = urwid.AttrMap(cancel_button, "body", "focus")
        buttons = [ok_button, cancel_button]
        button_grid = urwid.GridFlow(buttons, 10, 3, 1, "center")
        caption = urwid.Text(self.caption)
        caption = urwid.AttrMap(caption, "header", "")
        self.frame.header = urwid.Pile([caption])
        button_grid = urwid.AttrMap(button_grid, "header", "")
        divider = urwid.AttrMap(urwid.Divider(), "header", "header")
        self.frame.footer = urwid.Pile(
                [divider, button_grid, divider], focus_item=1)
        self.frame.set_focus("footer")
        # -----------------------------------------------------------
        return

    def button_no(self, data):
        self.result = DialogResult.NO
        raise urwid.ExitMainLoop()
        return

    def button_yes(self, data):
        self.result = DialogResult.YES
        raise urwid.ExitMainLoop()
        return

    def get_palette(self):
        palette = [
            ("body", "black", "light gray"),
            ("current_node", "dark red", "light gray"),
            ("focus", "light gray", "dark blue", "standout"),
            ("reveal_focus", "black", "dark cyan", "standout"),
            ("column_headers", "dark red", "light gray"),
            ("header", "light red", "black"),
            ('border', 'light red', 'black'),
        ]
        return palette

    def unhandled_input(self, key):
        if key == 'tab':
            button_grid = self.frame.footer[1]
            if button_grid.focus_position == 0:
                button_grid.focus_position = 1
                return None
            else:
                button_grid.focus_position = 0
                return None
        return key


class DialogResult(Enum):
    OK = 0
    CANCEL = 1
    YES = 2
    NO = 3


class FocusableText(urwid.WidgetWrap):
    def __init__(self, txt):
        self.t = urwid.Text(txt, wrap='clip')
        w = urwid.AttrMap(self.t, "body", "focus")
        urwid.WidgetWrap.__init__(self, w)

    @property
    def text(self):
        return self.t.text

    @text.setter
    def text(self, value):
        self.t.set_text(value)
        return

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class MyApp():
    def __init__(self, *args, **keywords):
        self.filename = "foo.xml"
        palette = self.get_palette()
        # tree_data = load_tree_data(filename=self.filename)
        # simple_tree = build_simple_tree(tree_data)
        simple_tree = construct_example_tree(children=3)
        arrow_tree = CollapsibleArrowTree(simple_tree)
        tree_box = CustomTreeBox(tree=arrow_tree, parent=self)
        app_title = "urwidtrees add/remove example"
        header = urwid.AttrMap(urwid.Text(app_title, align='center'), "header")
        footer = urwid.AttrMap(urwid.Text("Q to quit"), "focus")
        self.frame = urwid.Frame(tree_box, header=header, footer=footer)
        self.frame = urwid.AttrMap(self.frame, "body")
        self.loop = urwid.MainLoop(
                self.frame, palette=palette, unhandled_input=unhandled_input)
        return

    def get_palette(self):
        palette = [
            ("body", "black", "light gray"),
            ("current_node", "dark red", "light gray"),
            ("focus", "light gray", "dark blue", "standout"),
            ("reveal_focus", "black", "dark cyan", "standout"),
            ("column_headers", "dark red", "light gray"),
            ("header", "light red", "black"),
            ('border', 'light red', 'black'),
        ]
        return palette

    def start(self):
        self.loop.run()
        return


def build_simple_tree(tree_data=None):
    # -----------------------------------------------------------------
    tree = (FocusableText("root node"), [])
    # -----------------------------------------------------------------
    for data_object in tree_data:
        tree_path = data_object["tree_path"]
        leaf_names = tree_path.split("\\")
        parent_node = None
        current_node = tree
        for i in range(len(leaf_names)):
            # ---------------------------------------------------
            leaf = leaf_names[i]
            # ---------------------------------------------------
            if i == 0:
                i += 1  # root already added
                continue
            # ---------------------------------------------------
            # init list if needed
            if current_node[1] is None:
                current_node = (current_node[0], [])
                _, i = find_child(
                        current_node[0].text, child_list=parent_node[1])
                parent_node[1][i] = current_node
            # does this node already exist?
            child, _ = find_child(child=leaf, child_list=current_node[1])
            if child is not None:
                parent_node = current_node
                current_node = child
                continue
            # ---------------------------------------------------
            # is this the last node in nodes?
            if i + 1 == len(leaf_names):
                children = None
            else:
                children = []
            new_node = (FocusableText(leaf), children)
            current_node[1].append(new_node)
            parent_node = current_node
            current_node = new_node
            # ---------------------------------------------------
    # -----------------------------------------------------------------
    tree = SimpleTree([tree])
    # -----------------------------------------------------------------
    return tree


def find_child(child=None, child_list=None):
    for i in range(len(child_list)):
        if child == child_list[i][0].text:
            return child_list[i], i
    return None, None


def unhandled_input(key):
    if key in ["q", "Q"]:
        raise urwid.ExitMainLoop()


def construct_example_simpletree_structure(selectable_nodes=True, children=3):

    Text = FocusableText if selectable_nodes else urwid.Text

    # define root node
    tree = (Text("ROOT"), [])

    # define some children
    c = g = gg = 0  # counter
    for i in range(children):
        subtree = (Text("Child {0:d}".format(c)), [])
        # and grandchildren..
        for j in range(children):
            subsubtree = (Text("Grandchild {0:d}".format(g)), [])
            for k in range(children):
                leaf = (Text("Grand Grandchild {0:d}".format(gg)), None)
                subsubtree[1].append(leaf)
                gg += 1  # inc grand-grandchild counter
            subtree[1].append(subsubtree)
            g += 1  # inc grandchild counter
        tree[1].append(subtree)
        c += 1
    return tree


def construct_example_tree(selectable_nodes=True, children=2):
    # define a list of tree structures to be passed on to SimpleTree
    forrest = [
            construct_example_simpletree_structure(selectable_nodes, children)]

    # stick out test tree into a SimpleTree and return
    return SimpleTree(forrest)


if __name__ == "__main__":
    try:
        MyApp().start()
    except KeyboardInterrupt:
        print("\n\nKeyboard Interrupt...")
