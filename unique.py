from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

def get_data_chunks(file_path, delimiter):
    chunks = []
    chunk = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if delimiter in line:
                chunks.append(chunk)
                chunk = ''
            else:
                chunk += line
    
    chunks.append(chunk)
    
    return chunks

def group_similar(chunks, threshold):
    # Vectorize the chunks using TF-IDF
    vectorizer = TfidfVectorizer().fit_transform(chunks)
    vectors = vectorizer.toarray()

    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(vectors)

    groups = []
    visited = set()

    for i in range(len(chunks)):
        if i in visited:
            continue
        group = [i]
        visited.add(i)
        for j in range(i + 1, len(chunks)):
            if cosine_sim[i][j] >= threshold:
                group.append(j)
                visited.add(j)
        groups.append(group)

    return groups

def get_text_from_groups(clusters, chunks): 
    text = ''
    for idx, group in enumerate(clusters):
        text += f"Group {idx + 1}:\n"
        for i in group:
            lines = '\n'.join(f"{idx + 1}   " + line for line in chunks[i].splitlines())
            text += lines
            text += "\n\n"

    return text

def write_to_file(output_file, text):
    with open(output_file, "w") as file:
        file.write(text)

def grab_first_in_group(chunks, groups):
    text = ''
    for group in groups:
        text += chunks[group[0]] if group else ""
        text += "\n\n"
    return text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    delimiter = '------------------------------'

    text_delimited_file = os.path.join(data_dir, "text_delimited.txt")
    text_chunks = get_data_chunks(text_delimited_file, delimiter)
    grouped = group_similar(text_chunks, .90)
    uniqued_text = grab_first_in_group(text_chunks, grouped)
    # text = get_text_from_groups(grouped, text_chunks)
    
    text_output_file = os.path.join(data_dir, 'unique.text')
    write_to_file(text_output_file, uniqued_text)
    
    html_delimited_file = os.path.join(data_dir, "html_delimited.txt")
    html_chunks = get_data_chunks(html_delimited_file, delimiter)
    uniqed_html = grab_first_in_group(html_chunks, grouped)

    html_output_file = os.path.join(data_dir, 'unique.html')
    write_to_file(html_output_file, uniqed_html)