def get_iou_torch(ground_truth, pred):
    # Coordinates of the area of intersection.
    ix1 = torch.max(ground_truth[0][0], pred[0][0])
    iy1 = torch.max(ground_truth[0][1], pred[0][1])
    ix2 = torch.min(ground_truth[0][2], pred[0][2])
    iy2 = torch.min(ground_truth[0][3], pred[0][3])
    
    # Intersection height and width.
    i_height = torch.max(iy2 - iy1 + 1, torch.tensor(0.))
    i_width = torch.max(ix2 - ix1 + 1, torch.tensor(0.))
    
    area_of_intersection = i_height * i_width
    
    # Ground Truth dimensions.
    gt_height = ground_truth[0][3] - ground_truth[0][1] + 1
    gt_width = ground_truth[0][2] - ground_truth[0][0] + 1
    
    # Prediction dimensions.
    pd_height = pred[0][3] - pred[0][1] + 1
    pd_width = pred[0][2] - pred[0][0] + 1
    
    area_of_union = gt_height * gt_width + pd_height * pd_width - area_of_intersection
    
    iou = area_of_intersection / area_of_union
    
    return iou
  def main():
    get_iou_torch(ground_truth,pred)
    if _name_=='_main_':
      main()
