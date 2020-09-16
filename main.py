import csv
import json
import copy

def update_keypoint(row, index) -> {}:
  keypoint = {}
  index = index * 3 + 1
  keypoint.update({'x1': float(row[index]), 'y1': float(row[index + 1]), 'rate': float(row[index + 2])})
  return keypoint

def get_key_points(row) -> {}:
  res = {}
  keypoints = ['head', 'nose', 'coccyx', 'tail']
  index = 0
  for k in keypoints:
    res.update({keypoints[index]: update_keypoint(row, index)})
    index += 1
  return res

def update_coordinates(coordinates, v) -> {}:
  coordinates.update({'x1': v['x1']})
  coordinates.update({'x2': v['x2']})
  coordinates.update({'y1': v['y1']})
  coordinates.update({'y2': v['y2']})
  return coordinates

def update_objects(objects, attributes, category, children, coordinates, i_d, keypoints, rate) -> {}:
  objects[0].update({'attributes': attributes})
  objects[0].update({'category': category})
  objects[0].update({'children': children})
  objects[0].update({'coordinates': coordinates})
  objects[0].update({'id': i_d})
  objects[0].update({'keypoints': keypoints})
  objects[0].update({'rate': rate})
  return objects[0]

def get_current_row(reader):
  for i in range(3):
    next(reader)
  return next(reader)

def update_frame_annotation(frameIndex, objects) -> {}:
  tempDeepcopy = {}
  tempDeepcopy.update({'frame_index': int(frameIndex)})
  tempDeepcopy.update({'objects': (objects)})
  return tempDeepcopy

data = {}
temp = {}
frameAnnotations = {}
with open('Aeden_session_1_trial_1.csv', 'r') as csvFile, open('Aeden_session_1_trial_1.json', 'r') as jsonFile:
  reader = csv.reader(csvFile)
  currentRowCsv = get_current_row(reader)
  jsonData = json.load(jsonFile)
  count = 0
  index = 0
  objects = [{}]
  frameIndex = 0
  
  for d in jsonData['frame_annotations']:
    children = []
    coordinates = {}
    keypoints = {}
    category = ""
    i_d = 0
    rate = 0
    attributes = {}
    
    while int(d) > count:
      index = count
      frameIndex = count
      keypoints = get_key_points(currentRowCsv)
      count += 1
      currentRowCsv = next(reader)

      objects[0] = update_objects(objects, {}, None, [], {}, None, keypoints, None)
      tempDeepcopy = update_frame_annotation(frameIndex, objects)
      temp.update({str(index): copy.deepcopy(tempDeepcopy)})
      
    index = int(d)
    frameIndex = int(d)
    j = jsonData['frame_annotations'][str(d)]['dogs']
      
    for v in j:
      #get category
      category = v['category']
      #get children
      if v['children'] != None:
        children.append(v['children'])
      #get coordinates
      coordinates = update_coordinates(coordinates, v)
      #get id
      i_d = v['id']
      #get keypoints
      keypoints = get_key_points(currentRowCsv)
      #continue to next row in csv
      currentRowCsv = next(reader)
      #get rate
      rate = v['rate']
        
    objects[0] = update_objects(objects, attributes, category, children, coordinates, i_d, keypoints, rate)
    tempDeepcopy = update_frame_annotation(frameIndex, objects)
    temp.update({str(index): copy.deepcopy(tempDeepcopy)})
    
    count += 1

  #init file header
  res = {
        "existed_task": None,
        "video_name": "Aeden_session_1_trial_1.mp4",
        "fps": 29,
        "width": 1280,
        "height": 720
      }
  #update frame_annotations
  res.update({'frame_annotations': temp})
  data.update(res)
  #write data into target file
  with open("target.json", "w") as r:
    json.dump(data, r, indent=4)