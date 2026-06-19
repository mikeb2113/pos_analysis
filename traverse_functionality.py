def traverse(mapping_location):
    

#Need to be able to input starting location:
#This may look like [sentence_id],[location_in_sentence],[bundle_ids]]
#ex: ([73],[0],[0])
#This would lead into: ([73],[1],[0])
#Where itereating at the second index fails, you need to switch to itereation by the third index
#Where iterating at the third index fails, the sentence is over. Return a proposed starting location of ([74],[0],[0])