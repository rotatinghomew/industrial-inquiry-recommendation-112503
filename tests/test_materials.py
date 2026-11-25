"""从项目根目录执行资料契约检查。"""
from pathlib import Path
import json
import unittest

import numpy as np
from scipy import sparse

DATA = Path(__file__).resolve().parents[1] / "资料"

def load(name):
    """读取已经登记的 UTF-8 JSON 资料。"""
    with (DATA / f"{name}.json").open(encoding="utf-8") as source:
        return json.load(source)

KEYS = {'技术申请': 'request', '团队': 'team', '展示日志': 'exposure', '询价回函': 'id'}
REFERENCES = [('展示日志', 'request', '技术申请', 'request'), ('展示日志', 'team', '团队', 'team'), ('询价回函', 'exposure', '展示日志', 'exposure')]

class MaterialChecks(unittest.TestCase):
    def test_identity(self):
        """检查来源主键与登记范围。"""
        for collection, field in KEYS.items():
            with self.subTest(collection=collection):
                entries = load(collection)
                self.assertTrue(entries)
                values = [r[field] for r in entries]
                self.assertEqual(len(set(values)), len(entries))
                self.assertNotIn(None, values)

    def test_references(self):
        """核对资料表之间的引用，不改变原记录。"""
        for origin, source_field, target, target_field in REFERENCES:
            with self.subTest(origin=origin, field=source_field):
                codes = {r[target_field] for r in load(target)}
                for row in load(origin):
                    if row[source_field] is not None:
                        self.assertIn(row[source_field], codes)

    def test_data_runtime(self):
        """确认锁定的数组和稀疏矩阵依赖可用，并读取本项目资料。"""
        sizes = np.array([len(load(name)) for name in KEYS], dtype=np.int64)
        self.assertTrue(np.all(sizes > 0))
        self.assertEqual(int(sparse.csr_matrix(sizes.reshape(1, -1)).sum()), int(sizes.sum()))

    def test_related_material(self):
        """检查业务记录、变动与交接凭据是否实际存在。"""
        log = load("展示日志")
        for e in log:
            self.assertIn(e["team"], e["choice_set"])
            if e["conditional_first"] is not None:
                self.assertAlmostEqual(e["conditional_first"], 1 / len(e["choice_set"]), places=7)
        self.assertTrue(any(e["conditional_first"] is None for e in log))
        current = load("下一轮询价")
        rounds = {e["exposure"] for e in current["live_exposures"]}
        self.assertTrue({r["exposure"] for r in current["updates"] if "exposure" in r} <= rounds)
        teams = load("团队")
        self.assertLess(len({r["leader"] for r in teams}), len(teams))
