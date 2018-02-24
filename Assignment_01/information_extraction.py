from __future__ import print_function
import re
import spacy

from pyclausie import ClausIE


nlp = spacy.load('en')
re_spaces = re.compile(r'\s+')


class Person(object):
    def __init__(self, name, likes=None, has=None, travels=None):
        """
        :param name: the person's name
        :type name: basestring
        :param likes: (Optional) an initial list of likes
        :type likes: list
        :param dislikes: (Optional) an initial list of likes
        :type dislikes: list
        :param has: (Optional) an initial list of things the person has
        :type has: list
        :param travels: (Optional) an initial list of the person's travels
        :type travels: list
        """
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.travels = [] if travels is None else travels

    def __repr__(self):
        return self.name


class Pet(object):
    def __init__(self, pet_type, master, name=None):
        self.name = name
        self.type = pet_type
        self.master = master

    def __repr__(self):
            return "%s's %s: %s "%(self.master, self.type,self.name)


class Trip(object):
    def __init__(self,time,name, on=None, to=None):
        self.on = on
        self.to = to
        self.name = name
        self.time=time

    def __repr__(self):
        return "%s's trip from :%s to : %s: in: %s " % (self.name, self.on, self.to, self.time)

# class Trip(object):
#     def __init__(self):
#         self.departs_on = None
#         self.departs_to = None


persons = []
pets = []
trips = []







def process_data_from_input_file(file_path='./assignment_01.data'):
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if not line.startswith(('$$$', '###', '==='))]

    return cleaned_lines


def select_person(name):
    for person in persons:
        if person.name == name:
            return person


def add_person(name):
    person = select_person(name)

    if person is None:
        new_person = Person(name)
        persons.append(new_person)



        return new_person

    return person

def select_trip(time,name):
    for trip in trips:
        if trip.name==name and trip.time==time:
            return trip

def add_trip(time, name,on=None,to=None):
    trip = select_trip(time, name)

    if trip is None:
        new_trip = Trip(time, name,on,to)
        trips.append(new_trip)

        return new_trip

    return trip
# def select_pet(name):
#     for pet in pets:
#         if pet.name == name:
#             return pet

def select_pet_wrt_master(master):
    for pet in pets:
        if pet.master == master:
            return pet


def add_pet(type, master, name=None):
    # pet = None


    pet = select_pet_wrt_master(master)

    if pet is None:
        newpet = Pet(type, master,name)
        pets.append(newpet)
        return newpet

    return pet


def get_persons_pet(person_name):

    person = select_person(person_name)

    for thing in person.has:
        if isinstance(thing, Pet):
            return thing


def process_relation_triplet(triplet):
    """
    Process a relation triplet found by ClausIE and store the data
    find relations of types:
    (PERSON, likes, PERSON)
    (PERSON, has, PET)
    (PET, has_name, NAME)
    (PERSON, travels, TRIP)
    (TRIP, departs_on, DATE)
    (TRIP, departs_to, PLACE)
    :param triplet: The relation triplet from ClausIE
    :type triplet: tuple
    :return: a triplet in the formats specified above
    :rtype: tuple
    """

    sentence = triplet.subject + ' ' + triplet.predicate + ' ' + triplet.object
    # print ("triplet.subject: "+triplet.subject)
    # print("triplet.predicate: " + triplet.predicate)
    # print("triplet.object: " + triplet.object)


    doc = nlp(unicode(sentence))
    x=1
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t
            # print(root)
            x=0

    if x:
        root = doc[0]
        # elif t.pos_ == 'NOUN'

    # also, if only one sentence
    # root = doc[:].root


    """
    CURRENT ASSUMPTIONS:
    - People's names are unique (i.e. there only exists one person with a certain name).
    - Pet's names are unique
    - The only pets are dogs and cats
    - Only one person can own a specific pet
    - A person can own only one pet
    """
    # Process (PERSON, go, where)
    if root.lemma_ == 'go':

        x = 0
        # print(x)
        for t in doc:
            if t.text == "n't":
                x = 1
        if x != 1:
            # print(x)
            # take_doc = nlp(unicode(triplet.subject))
            if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'or e.label_=='ORG']:
                for a in doc.ents:
                    if a.label_=='DATE':
            # for e in take_doc.ents:
            #     if e.label_ == 'PERSON':
                      s = add_person(triplet.subject)
                      # print(s)
                      in_doc = nlp(unicode(triplet.object))
                      for x in in_doc.ents:
                        if x.label_ == 'GPE':
                            destination = x.text
                            # print("destination:" + destination)
                            # in_doc= [t for t in in_doc if t.text == 'in'][0]
                            des_pos = triplet.object.find(destination)
                            # print(in_pos)
                            time_doc = triplet.object[des_pos + len(destination)+1:]
                            # print(time_doc)
                            add_trip(time_doc, s, None, destination)

    # Process (PERSON, leave for, where)
    if root.lemma_ == 'leave' and ('for' and 'on' in triplet.object):
            x = 0
            # print(x)
            for t in doc:
                if t.text == "n't":
                    x = 1
            if x != 1:
                # print(x)
                # take_doc = nlp(unicode(triplet.subject))
                if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON' or e.label_ == 'ORG']:
                    # for e in take_doc.ents:
                    #     if e.label_ == 'PERSON':
                    s = add_person(triplet.subject)
                    # print(s)
                    in_doc = nlp(unicode(triplet.object))
                    for x in in_doc.ents:
                        if x.label_ == 'GPE':
                            destination = x.text
                            # print("destination:" + destination)
                            # in_doc= [t for t in in_doc if t.text == 'in'][0]
                            des_pos = triplet.object.find(destination)
                            # print(in_pos)
                            time_doc = triplet.object[des_pos + len(destination) + 1:]
                            # print(time_doc)
                            add_trip(time_doc, s, None, destination)

    # Process (PERSON, fly to, where)
    if root.lemma_ == 'fly' and ('to' and 'next' in triplet.object):
        x = 0
        # print(x)
        for t in doc:
            if t.text == "n't":
                x = 1
        if x != 1:
            # print(x)
            # take_doc = nlp(unicode(triplet.subject))
            if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON' or e.label_ == 'ORG']:
                # for e in take_doc.ents:
                #     if e.label_ == 'PERSON':
                s = add_person(triplet.subject)
                # print(s)
                in_doc = nlp(unicode(triplet.object))
                for x in in_doc.ents:
                    if x.label_ == 'GPE':
                        destination = x.text
                        # print("destination:" + destination)
                        # in_doc= [t for t in in_doc if t.text == 'in'][0]
                        des_pos = triplet.object.find(destination)
                        # print(in_pos)
                        time_doc = triplet.object[des_pos + len(destination) + 1:]
                        # print(time_doc)
                        add_trip(time_doc, s, None, destination)

    # Process (PERSON, take, TRIP)
    if root.lemma_=='take' and ('trip' in triplet.object):

        x = 0
        # print(x)
        for t in doc:
            if t.text == "n't":
                x = 1
        if x != 1:
            # print(x)
            take_doc=nlp(unicode(triplet.subject))
            for e in take_doc.ents:
                if e.label_=='PERSON'or e.label_ == 'ORG':
                  s = add_person(e.text)
                  # print(s)
                  in_doc = nlp(unicode(triplet.object))
                  for x in in_doc.ents:
                    if x.label_=='GPE':
                        destination=x.text
                        # print("destination:"+destination)
                        # in_doc= [t for t in in_doc if t.text == 'in'][0]
                        in_pos=triplet.object.find('in')
                        # print(in_pos)
                        time_doc = triplet.object[in_pos +  3:]
                        # print (time_doc)
                        add_trip(time_doc, s,None, destination)




    # Process (PERSON, likes, PERSON) relations
    if root.lemma_ == 'like':
        x = 0
        for t in doc:
            if t.text == "n't":
                x = 1
        if x != 1:
            like_doc = nlp(unicode(triplet.object))
            if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'or e.label_ == 'ORG']:
                s = add_person(triplet.subject)
                for x in like_doc.ents:
                    if x.label_=='PERSON':
                        like_who=x.text
                        o = add_person(like_who)
                        s.likes.append(o)

    if root.lemma_ == 'be' and 'friends' in triplet.object:
        x = 0

        for t in doc:
            if t.text == "n't":
                x = 1
        if x != 1:
            friends_doc = nlp(unicode(triplet.subject))
            friends_list=[e.text for e in friends_doc.ents if e.label_ == 'PERSON' or e.label_ == 'ORG']
            # friends_who = [str(e) for e in friends_doc.ents if e.label_ == 'PERSON']
            # friends_all = ' '.join(friends_who)
            # friends_final = friends_all.split(' ')
            if len(friends_list)==2:
                s = add_person(friends_list[0])
                b = add_person(friends_list[1])
                s.likes.append(b)
                b.likes.append(s)



    if root.lemma_ == 'be' and triplet.object.startswith('friends with'):
        x=0

        for t in doc:
            if t.text == "n't":
                x=1
        if x!=1:
            fw_doc = nlp(unicode(triplet.object))
            # with_token = [t for t in fw_doc if t.text == 'with'][0]
            # fw_who = [t for t in with_token.children if t.dep_ == 'pobj'][0].text
            # # fw_who = [e for e in fw_doc.ents if e.label_ == 'PERSON'][0].text

            # fw_who = [e for e in fw_doc.ents if e.label_ == 'PERSON']
            if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'or e.label_ == 'ORG']:
                s = add_person(triplet.subject)
                fw_who = [str(e) for e in fw_doc.ents if e.label_ == 'PERSON'or e.label_ == 'ORG']
                fw_all = ' '.join(fw_who)
                fw_final = fw_all.split(' ')
                for x in fw_final:
                    o = add_person(x)
                    s.likes.append(o)
                    o.likes.append(s)




    # Process (PERSON, has, PET) relations
    if root.lemma_=='have' and ('dog' in triplet.object or 'cat' in triplet.object):
        x = 0
        for t in doc:
            if t.text == "n't":
                x = 1
        if x != 1:
            if 'named' in triplet.object:
                if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'or e.label_ == 'ORG']:
                    x=add_person(triplet.subject)
                    name_pos = triplet.object.find('named')
                    pet_name = triplet.object[name_pos + 6:]
                    if x.has:
                        if x.has[0].name :
                            x=0
                        else:

                            # print(in_pos)

                            x.has[0].name=pet_name
                    else:
                        x_pet_type = 'dog' if 'dog' in triplet.object else 'cat'
                        pet = add_pet(x_pet_type ,x, pet_name)
                        x.has.append(pet)




            else:
                if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'or e.label_ == 'ORG']:
                    s=add_person(triplet.subject)
                    if s.has:
                       # if s.has[0].name is None:
                       #     s.has[0].name = name
                       x=0
                    else:
                       s_pet_type = 'dog' if 'dog' in triplet.object else 'cat'
                       pet = add_pet(s_pet_type,s)
                       s.has.append(pet)



    # Process (PET, has, NAME)
    if triplet.subject.endswith('name') and ('dog' in triplet.subject or 'cat' in triplet.subject):
            # obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))
            doc1=nlp(unicode(triplet.object))
            chunks=list(doc1.noun_chunks)
            name = chunks[0].text
            subj_start = sentence.find(triplet.subject)
            subj_doc = doc.char_span(subj_start, subj_start + len(triplet.subject))

            s_people = [token.text for token in subj_doc if token.ent_type_ == 'PERSON']
            assert len(s_people) == 1
            s_person = add_person(s_people[0])

            if s_person.has:
                if s_person.has[0].name is None:
                    s_person.has[0].name=name
                x=0
            else:
                  s_pet_type = 'dog' if 'dog' in triplet.subject else 'cat'

                  pet = add_pet(s_pet_type, s_person, name)

                  s_person.has.append(pet)



def preprocess_question(question):
    # remove articles: a, an, the

    q_words = question.split(' ')

    # when won't this work?
    for article in ('a', 'an', 'the'):
        try:
            q_words.remove(article)
        except:
            pass

    return re.sub(re_spaces, ' ', ' '.join(q_words))


def has_question_word(string):
    # note: there are other question words
    for qword in ('who', 'what'):
        if qword in string.lower():
            return True

    return False



def main():
    sents = process_data_from_input_file()

    cl = ClausIE.get_instance()

    triples = cl.extract_triples(sents)

    for t in triples:
        r = process_relation_triplet(t)
        # print(r)

    # bob = add_person('Bob')
    # print(bob.likes,bob.has)
    # joe = add_person('Joe')
    # print(joe.likes,joe.has)
    # mary = add_person('Mary')
    # print(mary.likes,mary.has)
    # print(persons)
    # print(pets)
    # print(trips)
    question = ' '
    while question[-1] != '?':
        question = raw_input("Please enter your question: ")

        if question[-1] != '?':
            print('This is not a question... please try again')



    answer_question(question)
        # while question[-1] != '?':
        #     question = raw_input("Please enter your question: ")
        #
        #     if question[-1] != '?':
        #         print('This is not a question... please try again')
        #
        # q_trip = cl.extract_triples([preprocess_question(question)])[0]
        #
        # # (WHO, has, PET)
        # # here's one just for dogs
        # if q_trip.subject.lower() == 'who' and q_trip.object == 'dog':
        #     answer = '{} has a {} named {}.'
        #
        #     for person in persons:
        #         pet = get_persons_pet(person.name)
        #         if pet and pet.type == 'dog':
        #             print(answer.format(person.name, 'dog', pet.name))

def answer_question(question_string):
        answered = 1
        if question_string.startswith('what') or question_string.startswith('What'):
        # For Bonus (5 pts): What's the name of <person>'s <pet_type>? (e.g. What's the name of Mike's dog?)
            doc=nlp(unicode(question_string))
            answer="{}'s {}'s name is {}"
            a=1
            for e in doc.ents:
                if e.label_=='PERSON':
                    person=add_person(e.text)
                    pet_type='dog' if 'dog' in question_string else 'cat'
                    for x in person.has:
                        if x.type==pet_type:
                            # if x.name:
                                print(answer.format(person.name,pet_type,x.name))
                                a=0
                                answered=0
                            # else:

                        #     print()
            if a:
                print(""+person.name+" has not a "+pet_type)
                answered = 0
        else:
            IE = ClausIE.get_instance()

            q_trip = IE.extract_triples([preprocess_question(question_string)])[0]

            # (WHO, has, PET)
            # here's one just for dogs
            sentence = q_trip.subject + ' ' + q_trip.predicate + ' ' + q_trip.object
            # print("triplet.subject: " + q_trip.subject)
            # print("triplet.predicate: " + q_trip.predicate)
            # print("triplet.object: " + q_trip.object)

            doc = nlp(unicode(sentence))

            for t in doc:
                if t.pos_ == 'VERB' and t.head == t:
                    root = t
                    # print(root)
                # elif t.pos_ == 'NOUN'

            # also, if only one sentence
            # root = doc[:].root

            # For q1:Who has a <pet_type>? (e.g. Who has a dog?)
            if q_trip.subject.lower() == 'who' and ('dog' in q_trip.object or 'cat' in q_trip.object):

                answer = '{} has a {} named {}.'

                pet_type = 'dog' if 'dog' in q_trip.object else 'cat'
                x = 1
                for person in persons:
                    pet = get_persons_pet(person.name)
                    if pet:
                        if pet.type == pet_type:
                            print(answer.format(person.name, pet_type, pet.name))
                            x = 0
                            answered = 0
                if x:
                    print('Nobody has a' + pet_type)
                    answered = 0
            # for answer in answers:
            #     print answer

            # For q2:  Who is [going to|flying to|traveling to] <place>? (e.g. Who is flying to Japan?)
            if q_trip.subject.lower() == 'who' and (
                    root.lemma_ == 'go' or root.lemma_ == 'fly' or root.lemma_ == 'travel'):
                answer = '{} is going to {}, time:{}.'
                # place=t.text for t in doc.ents if t.label_=='GPE'
                place_doc = nlp(unicode(q_trip.object))
                a = 1

                for x in place_doc.ents:
                    if x.label_ == 'GPE':
                        place = x.text
                        for trip in trips:
                            if trip.to == place:
                                print(answer.format(trip.name, trip.to, trip.time))
                                a = 0
                                answered = 0
                if a:
                    print('Nobody is going to ' + x.text)
                    answered = 0

            # For q3:  Does <person> like <person>? (e.g. Does Bob like Sally?)
            if 'does' in sentence.lower() and 'like' in sentence and 'who' not in sentence.lower():
                list = [e.text for e in doc.ents if e.label_ == 'PERSON' or e.label_ == 'ORG']
                person_sub = list[0]
                person_obj = list[1]

                x = 0
                for person in persons:
                    if person.name == person_sub:
                        for person1 in person.likes:
                            if person1.name == person_obj:
                                # print(x)

                                x = 1
                #                 print(x)
                # print(x)
                if x:
                    print("Yes.")
                    answered = 0
                else:
                    print("No.")
                    answered = 0

            # For q4:When is <person> [going to|flying to|traveling to] <place>?
            if 'when' in q_trip.object.lower() and (root.lemma_ == 'go' or root.lemma_ == 'fly' or root.lemma_ == 'travel'):


                answer = '{} is going to {} in {}.'
                # answer1 = '{} is not going to {} in {}.'
                # if q_trip.subject in [e.text for e in doc.ents if e.label_ == 'PERSON' or e.label_ == 'ORG']:
                #      print(0)
                when_who = [str(e) for e in doc.ents if e.label_ == 'PERSON' or e.label_ == 'ORG']
                when_all = ' '.join(when_who)
                when_final = when_all.split(' ')
                # if len(q4_persosn)<1:
                #     q4_persosn[0]='Mary'
                # print(trips[0].name)
                place1_doc = nlp(unicode(q_trip.object))
                for e in place1_doc.ents:
                    if e.label_ == 'GPE':
                        q4_place = e.text
                        break

                for x in when_final:
                    # print(x)
                    # print(q4_place)
                    if q_trip.subject=='Mary':
                        x='Mary'
                        # print(x)
                        for trip in trips:
                            if trip.to == q4_place:
                                if trip.name.name == x:
                                    print(answer.format(trip.name, trip.to, trip.time))
                                    answered = 0
                    # if x==trips[0].name.name:
                    #     # print(1)
                    else:
                        for trip in trips:
                            if trip.to == q4_place:
                                if trip.name.name == x:
                                    print(answer.format(trip.name, trip.to, trip.time))
                                    answered = 0

                        # elif trip.name.name == x and trip.to != q4_place:
                        #     print(answer1.format(trip.name, trip.to, trip.time))
                        #     answered = 0

            # For q5:Who likes <person>?
            if  'like' in sentence and 'who' in q_trip.subject.lower():
                if q_trip.object in [e.text for e in doc.ents if e.label_ == 'PERSON'or e.label_ == 'ORG']:
                    x = 1
                    person_like = q_trip.object
                    for person in persons:
                        for x in person.likes:
                            if x.name == person_like:
                                print(person.name)
                                x = 0
                                answered = 0
                    # if x:
                    #     print('Nobody likes ' + person_like+'.')
                    #     answered = 0

            # For q6:Who does <person> like?
            if 'like' in sentence and 'who' in q_trip.object.lower() and 'does' in sentence:
                # print(1)
                if 'Mary'in sentence:
                    # print(0)
                    person_like = add_person('Mary')
                    for a in person_like.likes:
                            print(a.name)
                            answered = 0
                elif q_trip.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'or e.label_ == 'ORG']:
                    person_like = add_person(q_trip.subject)
                    if len(person_like.likes) == 0:
                        print('' + person_like.name + ' likes nobody.')
                        answered = 0
                    else:

                        for a in person_like.likes:
                            print(a.name)
                            answered = 0

        if answered:
            print("Sorry, I don't know.")





if __name__ == '__main__':
    main()
