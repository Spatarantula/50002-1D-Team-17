import graphviz


def listify(a) -> list:
    if a is None:
        return a

    if not isinstance(a, list):
        return [a]
    return a


def extend_len(a: list[str], length: int) -> list:
    if len(a) == 1:
        return [a[0] for _ in range(length)]
    return a


class StateOutput:
    outputs = {
        "we",
        "ra",
        "rb",
        "rc",
        "literal",
        "asel",
        "bsel",
        "ra2sel",
        "wdsel",
        "alufn",
        "start",
        "finished",
        "state",
    }
    def __init__(
        self,
        we: str | list[str] = None,
        ra: str | list[str] = None,
        rb: str | list[str] = None,
        rc: str | list[str] = None,
        literal: str | list[str] = None,
        asel: str | list[str] = None,
        bsel: str | list[str] = None,
        ra2sel: str | list[str] = None,
        wdsel: str | list[str] = None,
        alufn: str | list[str] = None,
        start: str | list[str] = None,
        finished: str | list[str] = None,
        state: str | list[str] = None,

        we_label: str = None,
        ra_label: str = None,
        rb_label: str = None,
        rc_label: str = None,
        literal_label: str = None,
        asel_label: str = None,
        bsel_label: str = None,
        ra2sel_label: str = None,
        wdsel_label: str = None,
        alufn_label: str = None,
        start_label: str = None,
        finished_label: str = None,
        state_label: str = None,
    ):
        self.we = listify(we)
        self.ra = listify(ra)
        self.rb = listify(rb)
        self.rc = listify(rc)
        self.literal = listify(literal)
        self.asel = listify(asel)
        self.bsel = listify(bsel)
        self.ra2sel = listify(ra2sel)
        self.wdsel = listify(wdsel)
        self.alufn = listify(alufn)
        self.start = listify(start)
        self.finished = listify(finished)
        self.state = listify(state)

        self.we_label = we_label
        self.ra_label = ra_label
        self.rb_label = rb_label
        self.rc_label = rc_label
        self.literal_label = literal_label
        self.asel_label = asel_label
        self.bsel_label = bsel_label
        self.ra2sel_label = ra2sel_label
        self.wdsel_label = wdsel_label
        self.alufn_label = alufn_label
        self.start_label = start_label
        self.finished_label = finished_label
        self.state_label = state_label

    def __str__(self):
        attrs = []

        if self.we is not None:
            attrs.append(f"we = {' | '.join(self.we) if self.we_label is None else self.we_label }")
        if self.ra is not None:
            attrs.append(f"ra = {' | '.join(self.ra) if self.ra_label is None else self.ra_label }")
        if self.rb is not None:
            attrs.append(f"rb = {' | '.join(self.rb) if self.rb_label is None else self.rb_label }")
        if self.rc is not None:
            attrs.append(f"rc = {' | '.join(self.rc) if self.rc_label is None else self.rc_label }")
        if self.literal is not None:
            attrs.append(f"literal = {' | '.join(self.literal) if self.literal_label is None else self.literal_label }")
        if self.asel is not None:
            attrs.append(f"asel = {' | '.join(self.asel) if self.asel_label is None else self.asel_label }")
        if self.bsel is not None:
            attrs.append(f"bsel = {' | '.join(self.bsel) if self.bsel_label is None else self.bsel_label }")
        if self.ra2sel is not None:
            attrs.append(f"ra2sel = {' | '.join(self.ra2sel) if self.ra2sel_label is None else self.ra2sel_label }")
        if self.wdsel is not None:
            attrs.append(f"wdsel = {' | '.join(self.wdsel) if self.wdsel_label is None else self.wdsel_label }")
        if self.alufn is not None:
            attrs.append(f"alufn = {' | '.join(self.alufn) if self.alufn_label is None else self.alufn_label }")
        if self.start is not None:
            attrs.append(f"start = {' | '.join(self.start) if self.start_label is None else self.start_label }")
        if self.finished is not None:
            attrs.append(f"finished = {' | '.join(self.finished) if self.finished_label is None else self.finished_label }")
        if self.state is not None:
            attrs.append(f"state = {' | '.join(self.state) if self.state_label is None else self.state_label }")

        return ";\n".join(attrs)


class TransitionRule:
    def  __init__(self, cond: str | list[str], true_state: str | list[str], false_state: str = None, label: str = None, inv_label: str = None):
        cond = listify(cond)
        self.condition = cond
        self.label = " | ".join(cond) if label is None else label
        if isinstance(true_state, list):
            self.true_state = true_state
        else:
            self.true_state = [true_state]

        self.branch = False
        if false_state:
            self.inverse = map(lambda x: x.replace("==", "!="), cond)
            self.inv_label = " | ".join(self.inverse) if inv_label is None else inv_label
            self.false_state = false_state
            self.branch = True


class StateMachine:
    def __init__(self):
        self.transition = {}
        self.std = graphviz.Digraph('state_transition_diagram', filename = 'fsm.gv')

    def add_state(self, name: str, output: StateOutput, transition: TransitionRule = None):

        self.std.node(name, label = f"{name}\n{output}")

        if transition is not None:
            if len(transition.true_state) == 1:
                self.std.edge(name, transition.true_state[0], label = transition.label)
            else:
                assert len(transition.true_state) == len(transition.condition)
                for ts, cond in zip(transition.true_state, transition.condition):
                    self.std.edge(name, ts, label = cond)

            if transition.branch:
                self.std.edge(name, transition.false_state, label = transition.inv_label)

        self.transition[name] = transition, output

    def get_lucid_code(self):
        lucid_code = []

        for state, (rule, out) in self.transition.items(): # type: str, (TransitionRule, StateOutput)
            lucid_code.append(f"game_state.{state}:")

            out_ls = {a: getattr(out, a) for a in StateOutput.outputs if getattr(out, a) is not None}

            out_lists = list(filter(lambda x: len(x[1]) > 1, out_ls.items()))

            length = 1
            if len(out_lists) > 0:
                length = len(out_lists[0][1])
                for a, ls in out_lists:
                    if len(ls) != length:
                        raise IndexError(f"attribute {a} not eq length")

            if len(rule.condition) > 1 and len(rule.condition) != length:
                raise IndexError(f"Transition Rule {rule.condition[0]} not eq length")

            conditions = extend_len(rule.condition, length)
            attr_maps = {attr: extend_len(val, length) for attr, val in out_ls.items()}

            if len(rule.true_state) > 1 and len(rule.true_state) != length:
                raise IndexError(f"Transition Rule {rule.true_state[0]} not eq length")

            true_state = extend_len(rule.true_state, length)

            placed_rb = False
            placed_fin = False
            for condition, *attribs, ts in zip(conditions, *attr_maps.values(), true_state):

                if not placed_rb and "rb_data" in condition:
                    lucid_code.append(f"  rb = {attr_maps['rb'][0]};")
                    placed_rb = True
                if not placed_fin and "finished" in attr_maps:
                    lucid_code.append(f"  finished = {attr_maps['finished'][0]};")
                    placed_fin = True

                ind = ""
                if condition != "always":
                    lucid_code.append(f"  if({condition}) {{")
                    ind = "  "

                for attrib, val in zip(attr_maps.keys(), attribs):
                    lucid_code.append(ind+f"  {attrib} = {val};")
                lucid_code.append(ind+f"  game_state.d = game_state.{ts};")

                if condition != "always":
                    lucid_code.append(f"  }}")
                    if rule.branch:
                        lucid_code[-1] += " else {"

                        for attrib, val in zip(attr_maps.keys(), attribs):
                            lucid_code.append(ind + f"  {attrib} = {val};")
                        lucid_code.append(ind + f"  game_state.d = game_state.{rule.false_state};")

                        lucid_code.append(f"  }}")

        return "\n".join(lucid_code)

    def generate_fsm_diagram(self):
        self.std.view()


A = StateMachine()

A.add_state(
    'START',
    StateOutput(start = "1"),
    TransitionRule("|c{button_0, button_asterisk, button_hash}", "SELECT_BOX_P1", label = " 0, * or # pressed")
)

size = [-1, "small", "med", "large"]
size_p1 = [-1, "1", "5", "9"]
size_p2 = [-1, "2", "6", "10"]

A.add_state(
    'SELECT_BOX_P1',
    StateOutput(
        ra = [f"regfile_addr.box{y}{x}" for y in range(3) for x in range(3)],
        ra_label = "0x00-0x09",
        rc = "regfile_addr.box_addr",
        alufn = "alu_op_code.t_a",
        we = "1",
    ),
    TransitionRule([f"button_{b+1}" for b in range(9)], "SELECT_SIZE_P1", label = " buttons 1-9 pressed"),
)

A.add_state(
    'SELECT_SIZE_P1',
    StateOutput(
        asel = "1",
        rb = [*[f"regfile_addr.pieces_remaining_{size[s]}_p1" for s in range(1, 4)], "0"],
        rb_label = "0x09-0x0D/0",
        rc = [*["regfile_addr.temp1" for _ in range(3)], "regfile_addr.box_addr"],
        rc_label = "regfile_addr.temp1/box_addr",
        alufn = [*["alu_op_code.lt" for _ in range(3)], "alu_op_code.t_a"],
        alufn_label = "alu_op_code.lt/t_a",
        we = "1",
    ),
    TransitionRule([f"button_{char}" for char in 'abcd'], [*[f"CHECK_SIZE_{size[s].upper()}_P1" for s in range(1, 4)], "SELECT_BOX_P1"]),
)

for s in range(1, 4):
    A.add_state(
        f'CHECK_SIZE_{size[s].upper()}_P1',
        StateOutput(
            literal = f"{size_p1[s]}",
            bsel = "1",
            rb = "regfile_addr.temp1",
            rc = "regfile_addr.selected_size_p1",
            alufn = "alu_op_code.t_b",
            we = "rb_data[0]",
        ),
        TransitionRule("rb_data == 0", true_state = "SELECT_BOX_P1", false_state = "VALIDATE_PLACEMENT_P1_PT1"),
    )

A.add_state(
    f'VALIDATE_PLACEMENT_P1_PT1',
    StateOutput(
        ra = "rb_data[4:0]",
        rb = "regfile_addr.box_addr",
        rc = "regfile_addr.temp2",
        alufn = "alu_op_code.t_a",
        we = "1"
    ),
    TransitionRule("always", true_state = "VALIDATE_PLACEMENT_P1_PT2"),
)

A.add_state(
    f'VALIDATE_PLACEMENT_P1_PT2',
    StateOutput(
        ra = "regfile_addr.selected_size_p1",
        rb = "regfile_addr.temp2",
        rc = "regfile_addr.temp3",
        alufn = "alu_op_code.sub",
        we = "1"
    ),
    TransitionRule("always", true_state = "VALIDATE_PLACEMENT_P1_PT3"),
)

A.add_state(
    f'VALIDATE_PLACEMENT_P1_PT3',
    StateOutput(
        ra = "regfile_addr.temp3",
        literal = "2",
        bsel = "1",
        rc = "regfile_addr.temp3",
        alufn = "alu_op_code.ltq",
        we = "1"
    ),
    TransitionRule("always", true_state = "VALIDATE_PLACEMENT_P1_PT4"),
)

A.add_state(
    f'VALIDATE_PLACEMENT_P1_PT4',
    StateOutput(
        rb = "regfile_addr.temp3",
    ),
    TransitionRule("rb_data == 0", true_state = "PLACE_PIECE_P1", false_state = "SELECT_BOX_P1"),
)

A.add_state(
    f'PLACE_PIECE_P1',
    StateOutput(
        ra = "regfile_addr.box_addr",
        rb = "regfile_addr.selected_size_p1",
        ra2sel = "1",
        alufn_label = "alu_op_code.t_b",
        we = "1"
    ),
    TransitionRule("always", true_state = "COMPLETE_ROW_0_CHECK_BOX_00_P1"),
)

for j in range(3):
    for i in range(3):
        if j < 2:
            if i == 0:
                tr = TransitionRule("always", true_state = f"COMPLETE_ROW_{j}_CHECK_BOX_{j}{i + 1}_P1")
            elif i == 1:
                tr = TransitionRule(
                    "rb_data == 0",
                    true_state = f"COMPLETE_ROW_{j + 1}_CHECK_BOX_{j + 1}0_P1",
                    false_state = f"COMPLETE_ROW_{j}_CHECK_BOX_{j}{i + 1}_P1"
                )
            else:
                tr = TransitionRule(
                    "rb_data == 0",
                    true_state = f"COMPLETE_ROW_{j + 1}_CHECK_BOX_{j + 1}0_P1",
                    false_state = f"HAS_P1_WON"
                )
        else:
            if i == 0:
                tr = TransitionRule("always", true_state = f"COMPLETE_ROW_{j}_CHECK_BOX_{j}{i + 1}_P1")
            elif i == 1:
                tr = TransitionRule(
                    "rb_data == 0",
                    true_state = f"COMPLETE_COL_0_CHECK_BOX_00_P1",
                    false_state = f"COMPLETE_ROW_{j}_CHECK_BOX_{j}{i + 1}_P1"
                )
            else:
                tr = TransitionRule(
                    "rb_data == 0",
                    true_state = f"COMPLETE_COL_0_CHECK_BOX_00_P1",
                    false_state = f"HAS_P1_WON"
                )
        A.add_state(
            f'COMPLETE_ROW_{j}_CHECK_BOX_{j}{i}_P1',
            StateOutput(
                ra = "regfile_addr.box_addr",
                rb = "regfile_addr.temp4",
                rc = "regfile_addr.temp4",
                literal = "2",
                bsel = "1",
                alufn = "alu_op_code.mod",
                we = "1"
            ),
            tr,
        )

for i in range(3):
    for j in range(3):
        if j < 2:
            if i == 0:
                tr = TransitionRule("always", true_state = f"COMPLETE_COL_{j}_CHECK_BOX_{j}{i + 1}_P1")
            elif i == 1:
                tr = TransitionRule(
                    "rb_data == 0",
                    true_state = f"COMPLETE_COL_{j + 1}_CHECK_BOX_{j + 1}0_P1",
                    false_state = f"COMPLETE_COL_{j}_CHECK_BOX_{j}{i + 1}_P1"
                )
            else:
                tr = TransitionRule(
                    "rb_data == 0",
                    true_state = f"COMPLETE_COL_{j + 1}_CHECK_BOX_{j + 1}0_P1",
                    false_state = f"HAS_P1_WON"
                )
        else:
            if i == 0:
                tr = TransitionRule("always", true_state = f"COMPLETE_COL_{j}_CHECK_BOX_{j}{i + 1}_P1")
            elif i == 1:
                tr = TransitionRule(
                    "rb_data == 0",
                    true_state = f"COMPLETE_DIA_0_CHECK_BOX_00_P1",
                    false_state = f"COMPLETE_COL_{j}_CHECK_BOX_{j}{i + 1}_P1"
                )
            else:
                tr = TransitionRule(
                    "rb_data == 0",
                    true_state = f"COMPLETE_DIA_0_CHECK_BOX_00_P1",
                    false_state = f"HAS_P1_WON"
                )
        A.add_state(
            f'COMPLETE_COL_{j}_CHECK_BOX_{j}{i}_P1',
            StateOutput(
                ra = "regfile_addr.box_addr",
                rb = "regfile_addr.temp4",
                rc = "regfile_addr.temp4",
                literal = "2",
                bsel = "1",
                alufn = "alu_op_code.mod",
                we = "1"
            ),
            tr,
        )

for i in range(3):
    if i == 0:
        tr = TransitionRule("always", true_state = f"COMPLETE_DIA_0_CHECK_BOX_{i+1}{i+1}_P1")
    elif i == 1:
        tr = TransitionRule(
            "rb_data == 0",
            true_state = f"COMPLETE_DIA_1_CHECK_BOX_20_P1",
            false_state = f"COMPLETE_DIA_0_CHECK_BOX_{i+1}{i+1}_P1"
        )
    else:
        tr = TransitionRule(
            "rb_data == 0",
            true_state = f"COMPLETE_DIA_1_CHECK_BOX_20_P1",
            false_state = f"HAS_P1_WON"
        )
    A.add_state(
        f'COMPLETE_DIA_0_CHECK_BOX_{i}{i}_P1',
        StateOutput(
            ra = "regfile_addr.box_addr",
            rb = "regfile_addr.temp4",
            rc = "regfile_addr.temp4",
            literal = "2",
            bsel = "1",
            alufn = "alu_op_code.mod",
            we = "1"
        ),
        tr,
    )

for i in range(3):
    if i == 0:
        tr = TransitionRule("always", true_state = f"COMPLETE_DIA_1_CHECK_BOX_{2-(i+1)}{i+1}_P1")
    elif i == 1:
        tr = TransitionRule(
            "rb_data == 0",
            true_state = f"SELECT_BOX_P2",
            false_state = f"COMPLETE_DIA_1_CHECK_BOX_{2-(i+1)}{i+1}_P1"
        )
    else:
        tr = TransitionRule(
            "rb_data == 0",
            true_state = f"SELECT_BOX_P2",
            false_state = f"HAS_P1_WON"
        )
    A.add_state(
        f'COMPLETE_DIA_1_CHECK_BOX_{2-i}{i}_P1',
        StateOutput(
            ra = "regfile_addr.box_addr",
            rb = "regfile_addr.temp4",
            rc = "regfile_addr.temp4",
            literal = "2",
            bsel = "1",
            alufn = "alu_op_code.mod",
            we = "1"
        ),
        tr,
    )

A.add_state(
    f'HAS_P1_WON',
    StateOutput(
        rb = "regfile_addr.temp4",
    ),
    TransitionRule(
        "rb_data == 0",
        true_state = f"SELECT_BOX_P2",
        false_state = f"DECLARE_P1_WINNER"
    ),
)

# BREAK POINT

A.add_state(
    'SELECT_BOX_P2',
    StateOutput(
        ra = [f"regfile_addr.box{y}{x}" for y in range(3) for x in range(3)],
        ra_label = "0x00-0x09",
        rc = "regfile_addr.box_addr",
        alufn = "alu_op_code.t_a",
        we = "1",
    ),
    TransitionRule([f"button_{b+1}" for b in range(9)], "SELECT_SIZE_P2", label = " buttons 1-9 pressed"),
)

A.add_state(
    'SELECT_SIZE_P2',
    StateOutput(
        asel = "1",
        rb = [*[f"regfile_addr.pieces_remaining_{size[s]}_p2" for s in range(1, 4)], "0"],
        rb_label = "0x09-0x0D/0",
        rc = [*["regfile_addr.temp1" for _ in range(3)], "regfile_addr.box_addr"],
        rc_label = "regfile_addr.temp1/box_addr",
        alufn = [*["alu_op_code.lt" for _ in range(3)], "alu_op_code.t_a"],
        alufn_label = "alu_op_code.lt/t_a",
        we = "1",
    ),
    TransitionRule([f"button_{char}" for char in 'abcd'], [*[f"CHECK_SIZE_{size[s].upper()}_P2" for s in range(1, 4)], "SELECT_BOX_P2"]),
)

for s in range(1, 4):
    A.add_state(
        f'CHECK_SIZE_{size[s].upper()}_P2',
        StateOutput(
            literal = f"{size_p2[s]}",
            bsel = "1",
            rb = "regfile_addr.temp1",
            rc = "regfile_addr.selected_size_p2",
            alufn = "alu_op_code.t_b",
            we = "rb_data[0]",
        ),
        TransitionRule("rb_data == 0", true_state = "SELECT_BOX_P2", false_state = "VALIDATE_PLACEMENT_P2_PT1"),
    )

A.add_state(
    f'VALIDATE_PLACEMENT_P2_PT1',
    StateOutput(
        ra = "rb_data[4:0]",
        rb = "regfile_addr.box_addr",
        rc = "regfile_addr.temp2",
        alufn = "alu_op_code.t_a",
        we = "1"
    ),
    TransitionRule("always", true_state = "VALIDATE_PLACEMENT_P2_PT2"),
)

A.add_state(
    f'VALIDATE_PLACEMENT_P2_PT2',
    StateOutput(
        ra = "regfile_addr.selected_size_p2",
        rb = "regfile_addr.temp2",
        rc = "regfile_addr.temp3",
        alufn = "alu_op_code.sub",
        we = "1"
    ),
    TransitionRule("always", true_state = "VALIDATE_PLACEMENT_P2_PT3"),
)

A.add_state(
    f'VALIDATE_PLACEMENT_P2_PT3',
    StateOutput(
        ra = "regfile_addr.temp3",
        literal = "2",
        bsel = "1",
        rc = "regfile_addr.temp3",
        alufn = "alu_op_code.ltq",
        we = "1"
    ),
    TransitionRule("always", true_state = "VALIDATE_PLACEMENT_P2_PT4"),
)

A.add_state(
    f'VALIDATE_PLACEMENT_P2_PT4',
    StateOutput(
        rb = "regfile_addr.temp3",
    ),
    TransitionRule("rb_data == 0", true_state = "PLACE_PIECE_P2", false_state = "SELECT_BOX_P2"),
)

A.add_state(
    f'PLACE_PIECE_P2',
    StateOutput(
        ra = "regfile_addr.box_addr",
        rb = "regfile_addr.selected_size_p2",
        ra2sel = "1",
        alufn_label = "alu_op_code.t_b",
        we = "1"
    ),
    TransitionRule("always", true_state = "COMPLETE_ROW_0_CHECK_BOX_00_P2"),
)

for j in range(3):
    for i in range(3):
        if j < 2:
            if i == 0:
                tr = TransitionRule("always", true_state = f"COMPLETE_ROW_{j}_CHECK_BOX_{j}{i + 1}_P2")
            elif i == 1:
                tr = TransitionRule(
                    "rb_data == 1",
                    true_state = f"COMPLETE_ROW_{j + 1}_CHECK_BOX_{j + 1}0_P2",
                    false_state = f"COMPLETE_ROW_{j}_CHECK_BOX_{j}{i + 1}_P2"
                )
            else:
                tr = TransitionRule(
                    "rb_data == 1",
                    true_state = f"COMPLETE_ROW_{j + 1}_CHECK_BOX_{j + 1}0_P2",
                    false_state = f"HAS_P2_WON"
                )
        else:
            if i == 0:
                tr = TransitionRule("always", true_state = f"COMPLETE_ROW_{j}_CHECK_BOX_{j}{i + 1}_P2")
            elif i == 1:
                tr = TransitionRule(
                    "rb_data == 1",
                    true_state = f"COMPLETE_COL_0_CHECK_BOX_00_P2",
                    false_state = f"COMPLETE_ROW_{j}_CHECK_BOX_{j}{i + 1}_P2"
                )
            else:
                tr = TransitionRule(
                    "rb_data == 1",
                    true_state = f"COMPLETE_COL_0_CHECK_BOX_00_P2",
                    false_state = f"HAS_P2_WON"
                )
        A.add_state(
            f'COMPLETE_ROW_{j}_CHECK_BOX_{j}{i}_P2',
            StateOutput(
                ra = "regfile_addr.box_addr",
                rb = "regfile_addr.temp4",
                rc = "regfile_addr.temp4",
                literal = "2",
                bsel = "1",
                alufn = "alu_op_code.mod",
                we = "1"
            ),
            tr,
        )

for i in range(3):
    for j in range(3):
        if j < 2:
            if i == 0:
                tr = TransitionRule("always", true_state = f"COMPLETE_COL_{j}_CHECK_BOX_{j}{i + 1}_P2")
            elif i == 1:
                tr = TransitionRule(
                    "rb_data == 1",
                    true_state = f"COMPLETE_COL_{j + 1}_CHECK_BOX_{j + 1}0_P2",
                    false_state = f"COMPLETE_COL_{j}_CHECK_BOX_{j}{i + 1}_P2"
                )
            else:
                tr = TransitionRule(
                    "rb_data == 1",
                    true_state = f"COMPLETE_COL_{j + 1}_CHECK_BOX_{j + 1}0_P2",
                    false_state = f"HAS_P2_WON"
                )
        else:
            if i == 0:
                tr = TransitionRule("always", true_state = f"COMPLETE_COL_{j}_CHECK_BOX_{j}{i + 1}_P2")
            elif i == 1:
                tr = TransitionRule(
                    "rb_data == 1",
                    true_state = f"COMPLETE_DIA_0_CHECK_BOX_00_P2",
                    false_state = f"COMPLETE_COL_{j}_CHECK_BOX_{j}{i + 1}_P2"
                )
            else:
                tr = TransitionRule(
                    "rb_data == 1",
                    true_state = f"COMPLETE_DIA_0_CHECK_BOX_00_P2",
                    false_state = f"HAS_P2_WON"
                )
        A.add_state(
            f'COMPLETE_COL_{j}_CHECK_BOX_{j}{i}_P2',
            StateOutput(
                ra = "regfile_addr.box_addr",
                rb = "regfile_addr.temp4",
                rc = "regfile_addr.temp4",
                literal = "2",
                bsel = "1",
                alufn = "alu_op_code.mod",
                we = "1"
            ),
            tr,
        )

for i in range(3):
    if i == 0:
        tr = TransitionRule("always", true_state = f"COMPLETE_DIA_0_CHECK_BOX_{i+1}{i+1}_P2")
    elif i == 1:
        tr = TransitionRule(
            "rb_data == 1",
            true_state = f"COMPLETE_DIA_1_CHECK_BOX_20_P2",
            false_state = f"COMPLETE_DIA_0_CHECK_BOX_{i+1}{i+1}_P2"
        )
    else:
        tr = TransitionRule(
            "rb_data == 1",
            true_state = f"COMPLETE_DIA_1_CHECK_BOX_20_P2",
            false_state = f"HAS_P2_WON"
        )
    A.add_state(
        f'COMPLETE_DIA_0_CHECK_BOX_{i}{i}_P2',
        StateOutput(
            ra = "regfile_addr.box_addr",
            rb = "regfile_addr.temp4",
            rc = "regfile_addr.temp4",
            literal = "2",
            bsel = "1",
            alufn = "alu_op_code.mod",
            we = "1"
        ),
        tr,
    )

for i in range(3):
    if i == 0:
        tr = TransitionRule("always", true_state = f"COMPLETE_DIA_1_CHECK_BOX_{2-(i+1)}{i+1}_P2")
    elif i == 1:
        tr = TransitionRule(
            "rb_data == 1",
            true_state = f"SELECT_BOX_P1",
            false_state = f"COMPLETE_DIA_1_CHECK_BOX_{2-(i+1)}{i+1}_P2"
        )
    else:
        tr = TransitionRule(
            "rb_data == 1",
            true_state = f"SELECT_BOX_P1",
            false_state = f"HAS_P2_WON"
        )
    A.add_state(
        f'COMPLETE_DIA_1_CHECK_BOX_{2-i}{i}_P2',
        StateOutput(
            ra = "regfile_addr.box_addr",
            rb = "regfile_addr.temp4",
            rc = "regfile_addr.temp4",
            literal = "2",
            bsel = "1",
            alufn = "alu_op_code.mod",
            we = "1"
        ),
        tr,
    )

A.add_state(
    f'HAS_P2_WON',
    StateOutput(
        rb = "regfile_addr.temp4",
    ),
    TransitionRule(
        "rb_data == 1",
        true_state = f"SELECT_BOX_P1",
        false_state = f"DECLARE_P2_WINNER"
    ),
)

A.add_state(
    f'DECLARE_P1_WINNER',
    StateOutput(
        literal = "1",
        bsel = "1",
        rc = "regfile_addr.winner",
        alufn_label = "alu_op_code.t_b",
        we = "1",
        finished = "1",
    ),
    TransitionRule("always", true_state = "END")
)

A.add_state(
    f'DECLARE_P2_WINNER',
    StateOutput(
        literal = "2",
        bsel = "1",
        rc = "regfile_addr.winner",
        alufn_label = "alu_op_code.t_b",
        we = "1",
        finished = "1",
    ),
    TransitionRule("always", true_state = "END")
)

A.add_state(
    f'END',
    StateOutput(
        finished = "1"
    ),
    TransitionRule("|c{button_0, button_asterisk, button_hash}", "START", label = " 0, * or # pressed")
)

A.generate_fsm_diagram()

with open("./fsm_cases.luc", "w") as file:
    for state in A.transition:
        print(state)
        file.write(state+"\n")

    a = A.get_lucid_code()
    file.write(a)
    print(a)
