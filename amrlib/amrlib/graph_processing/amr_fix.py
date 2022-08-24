import re

def get_var_concept_map(amrgraphstring):

    strings = re.findall(r"\([^ ]+ / [^ \)]+", amrgraphstring)

    vc = {}

    for string in strings:
        s = string.split(" / ")
        var = s[0].replace("(", "")
        concept = s[1].replace("\n", "")
        vc[var] = concept
        # if it has a name, then extend with name
        vc[var] = maybe_extend_name(var, concept, amrgraphstring)

    ### find all unlinked ###
    relsplits = re.split(r":[^ ]+ ", amrgraphstring)
    for tgt in relsplits[1:]:
        var = re.split(r"[ \n]", tgt)[0].replace("(", "").replace(")", "")
        if "'" in var or "\"" in var:
            continue
        if var not in vc:
            vc[var] = None

    return vc


def maybe_extend_name(var, concept, amrgraphstring):
    
    # get everything what follows after a concept
    rest = amrgraphstring.split(var + " / " + concept)[1]
    rest = " ".join(rest.split("\n")).split()
    brs = 0
    concept_subgraph = ""

    # get only the subgraph of the concept
    for i, elm in enumerate(rest):
        if i == 0 and elm.startswith(")"):
            # there is no subgraph, nothing needs to be done
            return concept
        if elm.startswith("("):
            # a subgraph begins, remember depth
            brs += 1

        # a subgraph ends, check how many depths are closed
        closebr = list(reversed(elm.split(")")))
        for case in closebr:
            if not case:
                brs -= 1
            else:
                break
        if brs in [0, 1]:
            # all name structures we are interested in are on level 0 or 1
            concept_subgraph += elm + " " 
        
        if brs < 0:
            # subgraph is fully complete
            concept_subgraph += closebr[-1]
            break
    
    concept_subgraph = concept_subgraph.strip()

    #get all name related structures
    name = concept_subgraph.split(" / name")
    if len(name) < 2:
        # there is no name, nothing needs be done
        return concept
    else:
        name = name[1]

    # get everything what follows the first name in subgraph
    varname = concept_subgraph.split(" / name")[0].split("(")[-1]
    name = name.split()
    
    # get opX values
    refined_concept_sg = ""
    for n in name:
        if not n.startswith(":op") and not n.startswith("'") and not n.startswith("\""):
            break
        else:
            refined_concept_sg += n + " "
    
    # build named concept substructure, return result
    refined_concept_sg = concept + " :name (" + varname + " / name " + refined_concept_sg.strip() + ")"
    return refined_concept_sg

        
def maybe_fix_unlinked_in_subgraph(amrgraphstring, amrgraphstring_sub):
    amrgraphstring_sub_old = amrgraphstring_sub
    try:
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
        amrgraphstring_sub = "\n".join([line.rstrip() for line in amrgraphstring_sub.split("\n")])
        print("subgraph fixed, all variables linked")
    except:
        print("something went wrong fixing the unlinked variables in subgraph, returning unlinked sugraph")
        amrgraphstring_sub = amrgraphstring_sub_old
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
            :ARG1 (xv8 / person :name (xv6 / name :op1 "Nelson"))
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

    amr = """(xv0 / have-concession-91
      :ARG1 (xv6 / possible-01
            :ARG1 (xv10 / walk-01
                  :ARG0 xv7
                  :destination (xv1 / ambulance)))
      :ARG2 (xv9 / strike-01
            :ARG1 (xv7 / person
                  :ARG0-of (xv3 / have-org-role-91
                        :ARG1 (xv2 / center)
                        :ARG2 (xv8 / president))
                  :name (xv5 / name
                        :op1 "Joseph"
                        :op2 "Torsella"))
            :ARG2 (xv4 / head)))"""
    amr_s = """(xv10 / walk-01
                  :ARG0 xv7
                  :destination (xv1 / ambulance)))"""
    amr_s_linked = """(xv10 / walk-01
                  :ARG0 (xv7 / person :name (xv5 / name :op1 "Joseph" :op2 "Torsella"))
                  :destination (xv1 / ambulance)))"""
    amr_s2 = """(xv10 / walk-01
                  :ARG0 xv7
                  :destination xv1)"""
    amr_s2_linked = """(xv10 / walk-01
                  :ARG0 (xv7 / person :name (xv5 / name :op1 "Joseph" :op2 "Torsella"))
                  :destination (xv1 / ambulance))"""
    assert amr_s_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s)
    assert amr_s2_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s2)
    assert sj(amr_s_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s))
    assert sj(amr_s2_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s2))
   
    print("test passed")

    amr = """# ::id 1460
# ::snt Senate confirms Janet Yellen as chair of US Federal Reserve
(xv0 / confirm-01
      :ARG0 (xv3 / government-organization
            :name (xv5 / name
                  :op1 "Senate"))
      :ARG1 (xv9 / person
            :name (xv6 / name
                  :op1 "Janet"
                  :op2 "Yellen"))
      :ARG2 (xv1 / chair-01
            :ARG0 xv9
            :ARG1 (xv4 / government-organization
                  :mod (xv2 / country
                        :name (xv8 / name
                              :op1 "US"))
                  :name (xv7 / name
                        :op1 "Federal"
                        :op2 "Reserve"))))"""
    amr_s = """(xv1 / chair-01
            :ARG0 xv9
            :ARG1 (xv4 / government-organization
                  :mod (xv2 / country
                        :name (xv8 / name
                              :op1 "US"))
                  :name (xv7 / name
                        :op1 "Federal"
                        :op2 "Reserve")))"""
    amr_s_linked = """(xv1 / chair-01
            :ARG0 (xv9 / person :name (xv6 / name :op1 "Janet" :op2 "Yellen"))
            :ARG1 (xv4 / government-organization
                  :mod (xv2 / country
                        :name (xv8 / name
                              :op1 "US"))
                  :name (xv7 / name
                        :op1 "Federal"
                        :op2 "Reserve")))"""
    amr_s2 = """(xv1 / chair-01
            :ARG0 xv9
            :ARG1 xv4)"""
    amr_s2_linked = """(xv1 / chair-01
            :ARG0 (xv9 / person :name (xv6 / name :op1 "Janet" :op2 "Yellen"))
            :ARG1 (xv4 / government-organization :name (xv7 / name :op1 "Federal" :op2 "Reserve")))"""
    
    assert amr_s_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s)
    assert amr_s2_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s2)
    assert sj(amr_s_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s))
    assert sj(amr_s2_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s2))
    
    print("test passed")

    amr = """(xv0 / set-02
      :ARG1 (xv1 / city
            :name (xv4 / name
                  :op1 "Hong"
                  :op2 "Kong"))
      :ARG2 (xv3 / march-01
            :ARG1 (xv2 / democracy)))"""
    amr_s = """(xv0 / set-02
      :ARG1 xv1
      :ARG2 xv1)"""
    amr_s_linked = """(xv0 / set-02
      :ARG1 (xv1 / city :name (xv4 / name :op1 "Hong" :op2 "Kong"))
      :ARG2 xv1)"""
    amr_s2 = """(xv0 / set-02
      :ARG1 xv1 
      :ARG2 (xv3 / march-01
            :ARG1 xv2))"""
    amr_s2_linked = """(xv0 / set-02
      :ARG1 (xv1 / city :name (xv4 / name :op1 "Hong" :op2 "Kong"))
      :ARG2 (xv3 / march-01
            :ARG1 (xv2 / democracy)))"""
    
    assert amr_s_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s)
    assert amr_s2_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s2)
    assert sj(amr_s_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s))
    assert sj(amr_s2_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s2))

    print("test passed")
    

    amr = """# ::id 1204
# ::snt From the start, however, the United States' declared goal was not just to topple Saddam but to stabilize Iraq and install a friendly government.
(xv0 / contrast-01
      :ARG2 (xv7 / goal
            :ARG1-of (xv4 / declare-02
                  :ARG0 (xv2 / country
                        :name (xv11 / name
                              :op1 "United"
                              :op2 "States")))
            :domain (xv1 / and
                  :op1 (xv17 / topple-01
                        :ARG0 xv2
                        :ARG1 (xv14 / person
                              :name (xv12 / name
                                    :op1 "Saddam")))
                  :op2 (xv15 / stabilize-01
                        :ARG0 xv2
                        :ARG1 (xv3 / country
                              :name (xv13 / name
                                    :op1 "Iraq")))
                  :op3 (xv10 / install-01
                        :ARG0 xv2
                        :ARG1 (xv8 / government-organization
                              :ARG0-of (xv5 / friendly-01)
                              :ARG0-of (xv9 / govern-01)))))
      :time (xv6 / from
            :op1 (xv16 / start-01)))"""

    amr_s = """(xv17 / topple-01
                        :ARG0 xv2
                        :ARG1 (xv14 / person
                              :name (xv12 / name
                                    :op1 "Saddam")))"""
    amr_s_linked = """(xv17 / topple-01
                        :ARG0 (xv2 / country :name (xv11 / name :op1 "United" :op2 "States"))
                        :ARG1 (xv14 / person
                              :name (xv12 / name
                                    :op1 "Saddam")))"""
    amr_s2 = """(xv1 / and
                  :op1 (xv17 / topple-01
                        :ARG0 xv2
                        :ARG1 (xv14 / person
                              :name (xv12 / name
                                    :op1 "Saddam")))
                  :op2 (xv15 / stabilize-01
                        :ARG0 xv2
                        :ARG1 xv3)
                  :op3 (xv10 / install-01
                        :ARG0 xv2
                        :ARG1 (xv8 / government-organization
                              :ARG0-of (xv5 / friendly-01)
                              :ARG0-of (xv9 / govern-01))))"""
    amr_s2_linked = """(xv1 / and
                  :op1 (xv17 / topple-01
                        :ARG0 (xv2 / country :name (xv11 / name :op1 "United" :op2 "States"))
                        :ARG1 (xv14 / person
                              :name (xv12 / name
                                    :op1 "Saddam")))
                  :op2 (xv15 / stabilize-01
                        :ARG0 xv2
                        :ARG1 (xv3 / country :name (xv13 / name :op1 "Iraq")))
                  :op3 (xv10 / install-01
                        :ARG0 xv2
                        :ARG1 (xv8 / government-organization
                              :ARG0-of (xv5 / friendly-01)
                              :ARG0-of (xv9 / govern-01))))"""
    
    assert amr_s_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s)
    assert amr_s2_linked == maybe_fix_unlinked_in_subgraph(amr, amr_s2)
    assert sj(amr_s_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s))
    assert sj(amr_s2_linked) == maybe_fix_unlinked_in_subgraph(sj(amr), sj(amr_s2))

    print("test passed")
    print("all tests passed")

if __name__ == '__main__':
    test()



