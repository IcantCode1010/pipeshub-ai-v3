# LLM Enhancement Todo

## 📋 Progress Tracker

### ✅ **Completed**
- **Week 1**: Enhanced task description to focus on synthesis and source clarity
  - Location: `app/modules/qna/prompt_templates.py` line 16
  - Change: Replaced generic "enterprise AI assistant" with synthesis-focused instruction
  - Status: ✅ **APPLIED & TESTED** - Confirmed working via test script

## 🚀 **Remaining Enhancements**

### **Week 2: Source Analysis Guideline**
**Target**: Add explicit source comparison instructions
**Location**: `app/modules/qna/prompt_templates.py` around line 44 (in `<instructions>` section)

**Add as new guideline #2** (shift existing guidelines down):
```python
2. Source Analysis:
- Compare information across different sources before concluding
- When sources disagree, note the disagreement explicitly: "Source [2] indicates X, while source [5] suggests Y"
- Consolidate similar information from multiple sources rather than repeating it
- Prioritize more recent or authoritative sources when conflicts arise
```

**Expected Impact**: 
- Active source comparison vs independent treatment
- Explicit conflict surfacing
- Information consolidation vs repetition
- Source quality reasoning

---

### **Week 3: Enhanced Reason Field**
**Target**: Improve reasoning explanation quality
**Location**: `app/modules/qna/prompt_templates.py` line 88 (in `<output_format>` section)

**Change**:
```python
# FROM:
"reason": "<Explain how the answer was derived using the chunks/user information and reasoning>",

# TO:
"reason": "<Explain how sources were analyzed and synthesized. Note any conflicts between sources or gaps in information.>",
```

**Expected Impact**:
- Better reasoning transparency
- Conflict documentation
- Gap identification
- Synthesis explanation

---

### **Week 4: Add Answer Type**
**Target**: Add synthesis classification
**Location**: `app/modules/qna/prompt_templates.py` line 90 (in `<output_format>` section)

**Change**:
```python
# FROM:
"answerMatchType": "<Exact Match | Derived From Chunks | Derived From User Info>",

# TO:
"answerMatchType": "<Exact Match | Derived From Chunks | Synthesized From Multiple Sources | Derived From User Info>",
```

**Expected Impact**:
- Clear synthesis identification
- Better response categorization
- Quality tracking capability

---

## 🧪 **Testing Strategy**

### **Behavioral Test Queries**
Create test cases that should trigger enhanced behaviors:

1. **Synthesis Testing**:
   - "What are our security policies across different departments?"
   - "How do our data retention policies vary by document type?"

2. **Conflict Detection**:
   - "What conflicts exist in our remote work guidelines?"
   - "Are there inconsistencies in our API documentation?"

3. **Source Comparison**:
   - "Compare guidance from HR vs Legal on employee data handling"
   - "What do different teams say about deployment procedures?"

### **Quality Metrics to Monitor**
- Reduced redundant sentences across sources
- Explicit conflict mentions: "Source [X] vs Source [Y]"
- Better source attribution with reasoning
- More analytical vs retrieval-focused responses

---

## 🎯 **Implementation Notes**

### **File Locations**
- Main prompt: `app/modules/qna/prompt_templates.py`
- Test script: `test_prompt_enhancement.py`

### **Testing Command**
```bash
cd "C:\projects\pipeshub-v3\pipeshub-ai\backend\python" && python test_prompt_enhancement.py
```

### **Rollback Strategy**
If any enhancement causes issues:
1. Git revert specific changes
2. Test with previous version
3. Adjust enhancement and retry

---

## 🔮 **Future Enhancements** (Post Week 4)

### **Phase 2: Reasoning Structure**
- Add reasoning checkpoints between LangGraph nodes
- Stream intermediate reasoning steps
- Include confidence scoring per reasoning step

### **Phase 3: Progressive Disclosure**
- Break answer generation: outline → draft → refinement → final
- Show search plan before execution
- Progressive citation building

### **Phase 4: Interactive Planning**
- Add planning node for execution strategy
- Allow user feedback on search approach
- Surface decision rationale for tool selection

---

## 📝 **Change Log**
- **2024**: Week 1 enhancement applied and tested successfully
- **Next**: Implement Week 2 source analysis guidelines