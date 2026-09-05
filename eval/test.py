from app.services.rag_service import retrieve
import json
from pathlib import Path
import time


def test():
    data = json.loads(Path("eval/questions.json").read_text("utf-8"))
    questions = data["questions"]
    success = [0]*len(questions)
    content_type_count = 0
    meaning_type_count = 0
    unrelated_type_count = 0
    content_success_count = 0
    meaning_success_count = 0
    unrelated_success_count = 0
    elapsed = []
    

    for i, question in enumerate(questions,start=0):
        start = time.time()
        context_list = retrieve(question["question"])
        elaspe = time.time() - start
        elapsed.append(elaspe)

        if question["type"] == "原文型":
            content_type_count += 1
        elif question["type"] == "语义型":
            meaning_type_count += 1
        elif question["type"] == "无关型":
            unrelated_type_count += 1

        if question["expected"]:
            expect_document_id = question["expected"]["document_id"]
            expect_chunk_id = question["expected"]["chunk_id"]
            for context_dict in context_list:
                if (context_dict["document_id"], context_dict["chunk_id"]) == (expect_document_id, expect_chunk_id):
                    success[i] = 1
                    if question["type"] == "原文型":
                        content_success_count += 1
                    elif question["type"] == "语义型":
                        meaning_success_count += 1
                    break
        else:
            if context_list == []:
                unrelated_success_count += 1
                success[i] = 1
            else:
                distances = []
                for context_dict in context_list:
                    distances.append(context_dict["distance"])
                print(f"第{i}个问题，该无关型未命中，返回上下文distance为:{distances}")

              


    success_count = sum(success)
    hit_rate = success_count/len(questions)
    content_hit_rate = content_success_count/content_type_count
    meaning_hit_rate = meaning_success_count/meaning_type_count
    unrelated_hit_rate = unrelated_success_count/unrelated_type_count
    first_load = elapsed[0]
    elapsed.pop(0)
    ave_latency = sum(elapsed)/(len(questions)-1)

    print(f"总命中率：{hit_rate}，内容类命中率：{content_hit_rate}，语义型命中率：{meaning_hit_rate}，无关型命中率：{unrelated_hit_rate};首次延迟：{first_load}平均延迟：{ave_latency}")



if __name__ == "__main__":
    test()


