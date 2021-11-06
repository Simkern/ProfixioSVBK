Attribute VB_Name = "Module1"
Sub Cleanup()
'
' Cleanup Macro
'
    Call TextToCol
    Call ColorDivs
    Call ColorDate
    Call SortDate
    
End Sub

Sub TextToCol()
'
' TextToCol Macro
'
    Columns("A:A").Select
    Selection.TextToColumns Destination:=Range("A1"), DataType:=xlDelimited, _
        TextQualifier:=xlDoubleQuote, ConsecutiveDelimiter:=False, Tab:=False, _
        Semicolon:=False, Comma:=True, Space:=False, Other:=False, FieldInfo _
        :=Array(Array(1, 1), Array(2, 1), Array(3, 1), Array(4, 1), Array(5, 1), Array(6, 1), _
        Array(7, 1), Array(8, 1), Array(9, 1), Array(10, 1), Array(11, 1), Array(12, 1)), _
        TrailingMinusNumbers:=True
    Range("A1").Select
    ActiveCell.FormulaR1C1 = "Match ID"
End Sub

Sub ColorDivs()
'
' Colouring Macro
'
' Div 1
    Range("C2:P1000").Select
    Selection.FormatConditions.Add Type:=xlExpression, Formula1:= _
        "=$C2=""Div 1"""
    Selection.FormatConditions(Selection.FormatConditions.Count).SetFirstPriority
    With Selection.FormatConditions(1).Interior
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorAccent6
        .TintAndShade = 0.799981688894314
    End With
    Selection.FormatConditions(1).StopIfTrue = False
' Div 2
    Range("C2:P1000").Select
    Selection.FormatConditions.Add Type:=xlExpression, Formula1:= _
        "=$C2=""Div 2"""
    Selection.FormatConditions(Selection.FormatConditions.Count).SetFirstPriority
    With Selection.FormatConditions(1).Interior
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorAccent5
        .TintAndShade = 0.799951170384838
    End With
    Selection.FormatConditions(1).StopIfTrue = False
' Div 3
    Range("C2:P1000").Select
    Selection.FormatConditions.Add Type:=xlExpression, Formula1:= _
        "=$C2=""Div 3"""
    Selection.FormatConditions(Selection.FormatConditions.Count).SetFirstPriority
    With Selection.FormatConditions(1).Interior
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorAccent4
        .TintAndShade = 0.799981688894314
    End With
    Selection.FormatConditions(1).StopIfTrue = False
' Past games
    Range("E2:P1000").Select
    Selection.FormatConditions.Add Type:=xlExpression, Formula1:= _
        "=NOT(ISBLANK($L2))"
    Selection.FormatConditions(Selection.FormatConditions.Count).SetFirstPriority
    With Selection.FormatConditions(1).Interior
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = -0.05
    End With
    Selection.FormatConditions(1).StopIfTrue = False
End Sub

Sub ColorDate()
Attribute ColorDate.VB_ProcData.VB_Invoke_Func = " \n14"
'
' ColorDate Macro
'
    Rows("1:1").Select
    Selection.Font.Bold = True
    With Selection.Interior
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = -0.149998474074526
        .PatternTintAndShade = 0
    End With
    Columns("B:B").Select
    With Selection.Interior
        .Pattern = xlSolid
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = -0.149998474074526
        .PatternTintAndShade = 0
    End With
    Columns("B:B").EntireColumn.AutoFit
End Sub

Sub SortDate()
'
' SortDate Macro
'
    Columns("B:B").Select
    ActiveWorkbook.Worksheets(1).Sort.SortFields.Clear
    ActiveWorkbook.Worksheets(1).Sort.SortFields.Add2 Key _
        :=Range("B1"), SortOn:=xlSortOnValues, Order:=xlAscending, DataOption:= _
        xlSortNormal
    With ActiveWorkbook.Worksheets(1).Sort
        .SetRange Range("A2:P1000")
        .Header = xlNo
        .MatchCase = False
        .Orientation = xlTopToBottom
        .SortMethod = xlPinYin
        .Apply
    End With
End Sub
