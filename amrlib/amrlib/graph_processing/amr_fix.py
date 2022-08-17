import re

def get_var_concept_map(amrgraphstring):

    strings = re.findall(r"\([^ ]+ / [^ \)]+", amrgraphstring)

    vc = {}

    for string in strings:
        s = string.split(" / ")
        var = s[0].replace("(", "")
        concept = s[1].replace("\n", "")
        vc[var] = concept

    ### find all unlinked ###

    relsplits = re.split(r":[^ ]+ ", amrgraphstring)
    for tgt in relsplits[1:]:
        var = re.split(r"[ \n]", tgt)[0].replace("(", "").replace(")", "")
        if "'" in var or "\"" in var:
            continue
        if var not in vc:
            vc[var] = None

    return vc

def maybe_fix_unlinked_in_subgraph(amrgraphstring, amrgraphstring_sub):

    vc = get_var_concept_map(amrgraphstring)
    vc_sub = get_var_concept_map(amrgraphstring_sub)
    for var in vc_sub:
        if vc_sub[var]:
            continue
        if not vc[var]:
            #unliked in both, means its a number/constant
            continue

        concept = vc[var]
        varconcept = "(" + var + " / " + concept + ")"
        if " " + var + " " in amrgraphstring_sub:
            amrgraphstring_sub = amrgraphstring_sub.replace(" " + var + " ", " " + varconcept + " ", 1)
        elif " " + var + "\n" in amrgraphstring_sub:
            amrgraphstring_sub = amrgraphstring_sub.replace(" " + var + "\n", " " + varconcept + "\n", 1)
        elif " " + var + ")" in amrgraphstring_sub:
            amrgraphstring_sub = amrgraphstring_sub.replace(" " + var + ")", " " + varconcept + ")", 1)
        else:
            raise IndexError("Can't replace unlinked var via supergraph")
    
    return amrgraphstring_sub


def test():

    # testing
    amr = """(xv0 / say-01
      :ARG0 (xv6 / person
            :name (xv4 / name
                  :op1 "Contes"))
      :ARG1 (xv2 / face-01
            :ARG0 (xv7 / person
                  :name (xv5 / name
                        :op1 "Druce")
                  :ARG1-of xv1)
            :ARG1 (xv1 / charge-05
                  :ARG2 (xv3 / murder-01))))"""
    amr_s = """(xv2 / face-01
            :ARG0 (xv7 / person
                  :name (xv5 / name
                        :op1 "Druce")
                  :ARG1-of xv1))"""
    amr_s_linked = """(xv2 / face-01
            :ARG0 (xv7 / person
                  :name (xv5 / name
                        :op1 "Druce")
                  :ARG1-of (xv1 / charge-05)))"""
    amr_s2 = """(xv0 / say-01
      :ARG0 (xv6 / person
            :name xv4
            :ARG1 xv1))"""
    amr_s2_linked = """(xv0 / say-01
      :ARG0 (xv6 / person
            :name (xv4 / name)
            :ARG1 (xv1 / charge-05)))"""
    
    def sj(string):
        return " ".join(" ".join(string.split("\n")).split())

    assert amr_s_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s)
    assert amr_s2_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s2)
    assert sj(amr_s_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s))
    assert sj(amr_s2_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s2))
    print("test passed")
    
    amr = """(xv0 / retry-01
      :ARG1 (xv8 / person
            :age (xv12 / temporal-quantity
                  :quant 27
                  :unit (xv13 / year))
            :name (xv6 / name
                  :op1 "Nelson"))
      :ARG2 (xv1 / charge-05
            :ARG1-of (xv11 / stem-02
                  :ARG2 (xv3 / disturb-01
                        :ARG0-of (xv5 / lead-03
                              :ARG2 (xv4 / die-01
                                    :ARG1 (xv9 / person
                                          :name (xv7 / name
                                                :op1 "Rosenbaum"))))))
            :ARG1 xv8
            :ARG2 (xv10 / right-05
                  :mod (xv2 / civil))))"""
    amr_s = """(xv1 / charge-05
            :ARG1-of (xv11 / stem-02
                  :ARG2 (xv3 / disturb-01
                        :ARG0-of (xv5 / lead-03
                              :ARG2 (xv4 / die-01
                                    :ARG1 (xv9 / person
                                          :name (xv7 / name
                                                :op1 "Rosenbaum"))))))
            :ARG1 xv8
            :ARG2 (xv10 / right-05
                  :mod (xv2 / civil)))"""
    amr_s_linked = """(xv1 / charge-05
            :ARG1-of (xv11 / stem-02
                  :ARG2 (xv3 / disturb-01
                        :ARG0-of (xv5 / lead-03
                              :ARG2 (xv4 / die-01
                                    :ARG1 (xv9 / person
                                          :name (xv7 / name
                                                :op1 "Rosenbaum"))))))
            :ARG1 (xv8 / person)
            :ARG2 (xv10 / right-05
                  :mod (xv2 / civil)))"""
    amr_s2 = """(xv0 / retry-01
      :ARG1 (xv8 / person
            :age (xv12 / temporal-quantity
                  :quant 27
                  :unit (xv13 / year))
            :name (xv6 / name
                  :op1 "Nelson"))
      :ARG2 xv1)"""
    amr_s2_linked = """(xv0 / retry-01
      :ARG1 (xv8 / person
            :age (xv12 / temporal-quantity
                  :quant 27
                  :unit (xv13 / year))
            :name (xv6 / name
                  :op1 "Nelson"))
      :ARG2 (xv1 / charge-05))"""
    assert amr_s_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s)
    assert amr_s2_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s2)
    assert sj(amr_s_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s))
    assert sj(amr_s2_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s2))
    print("test passed")
    print("all tests passed")

if __name__ == '__main__':
    test()



