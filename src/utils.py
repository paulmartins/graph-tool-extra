def sort_coordinates_for_linestring(tt):
  """
  Given a list of edges not necessarily in the right direction,
  reverse the direction if needed to obtain a path.
  tt = [
    (1,1), (0,0), 
    (2,2), (1,1), 
    (2,2), (3,3),
    (4,4), (3,3),
    (5,5), (4,4),
    (5,5), (6,6),
    (6,6), (7,7),
    (8,8), (7,7)
  ]
  is transformedd into
  [
    (0,0), (1,1), 
    (1,1), (2,2),
    (2,2), (3,3),
    (3,3), (4,4),
    ...
  ]
  """
    pairs = [tt[n:n+2] for n in range(0, len(tt), 2)]
    s = [pairs[0]]
    for ed in pairs[1:]:
        if s[-1][1] == ed[1]:
            s.append([ed[1], ed[0]])
        elif s[-1][0] == ed[0]:
            s[-1] = [s[-1][1], s[-1][0]]
            s.append(ed)
        elif s[-1][0] == ed[1]:
            s[-1] = [s[-1][1], s[-1][0]]
            s.append([ed[1], ed[0]])
        else:
            s.append(ed)
    return [i for p in s for i in p]
