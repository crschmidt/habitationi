def run():
    far = {}
    for i in ['A-1', 'A-2', 'B', 'SD-2']:
        far[i] = 0.5
    for i in ['C', 'SD-9', 'SD-10F', 'SD-10H']:
        far[i] = 0.6
    for i in ['C-1', 'BA-3', 'IB-2', 'O-1']:
        far[i] = .75
    for i in ['BA-1', 'SD-12']:
        far[i] = 1.0
    for i in ['C-1A', 'SD-5']:
        far[i] = 1.25
    for i in ['IA-1', 'IA', 'O-2A', 'SD-4A', 'SD-13']:
        far[i] = 1.5
    for i in ['C-2', 'C-2B', 'BA', 'BA-2', 'SD-8']:
        far[i] = 1.75
    for i in ['BC', 'O-2']:
        far[i] = 2.0
    for i in ['C-2A']:
        far[i] = 2.50
    for i in ['C-3', 'C-3A', 'C-3B', 'BB', 'BB-2', 'BC-1', 'IB-1', 'O-3', 'O-3A', 'SD-1', 'SD-6', 'SD-7']:
        far[i] = 3.0
    for i in ['IA-2', 'IB']:
        far[i] = 4.0
    far['BB-1'] = 3.25
    far['SD-11'] = 1.7
    far['SD-15'] = 3.5
    lot_area = {
            'A-1': 6000,
            'A-2': 4500,
            'C-1A': 1000,
            'BC': 500,
            'BC-1': 450,
            'IA-1': 700,
            'SD-8': 650,
            'SD-14': 800,
        }
    for i in ['IB-2', 'BA-1']:
        lot_area[i] = 1200
    for i in ['B', 'SD-2', 'SD-3']:
        lot_area[i] = 2500
    for i in ['C', 'SD-10F', 'SD-10H', 'SD-9']:
        lot_area[i] = 1800
    for i in ['C-1', 'BA-3']:
        lot_area[i] = 1500
    for i in ['C-2', 'C-2B', 'O-2', 'BA', 'BA-2', 'SD-4', 'SD-4A', 'SD-5', 'SD-11', 'SD-13']:
        lot_area[i] = 600
    for i in ['C-2A', 'C-3', 'C-3A', 'C-3B', 'BB', 'BB-1', 'BB-2', 'SD-1', 'SD-6', 'SD-7']:
        lot_area[i] = 300
    
    for i in ['A-1', 'A-2', 'B', 'C', 'C-1', 'C-1A', 'C-2', 'C-2A', 'C-2B', 'C-3', 'C-3A', 'C-3B']:
        print "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (i, far[i], lot_area[i])
run()        
